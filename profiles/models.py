import random
import string
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# ── Referral System ───────────────────────────────────────────────────────────

def _generate_referral_code():
    """Return a unique referral code in the format SE-XXXXXXXX."""
    chars = string.ascii_uppercase + string.digits
    while True:
        suffix = ''.join(random.choices(chars, k=8))
        code = f'SE-{suffix}'
        if not ReferralProfile.objects.filter(code=code).exists():
            return code


class ReferralBonus(models.Model):
    """Singleton — admin configures how much a referrer earns per new signup."""
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal('5.00'),
        help_text='Amount credited to the referrer\'s wallet when someone signs up with their code.'
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'amount': Decimal('5.00')})
        return obj

    def __str__(self):
        return f'Referral Bonus: ${self.amount} per signup'

    class Meta:
        verbose_name = 'Referral Bonus Setting'
        verbose_name_plural = 'Referral Bonus Setting'


class ReferralProfile(models.Model):
    """Holds a user's unique referral code."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_profile')
    code = models.CharField(max_length=20, unique=True, default=_generate_referral_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} — {self.code}'

    @property
    def total_referrals(self):
        return self.user.referrals_made.count()

    @property
    def total_earned(self):
        from django.db.models import Sum
        result = self.user.referrals_made.aggregate(total=Sum('reward_amount'))['total']
        return result or Decimal('0.00')


class ReferralRecord(models.Model):
    """Records each successful referral."""
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    reward_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.referred.username} referred by {self.referrer.username} (+${self.reward_amount})'

    class Meta:
        ordering = ['-created_at']


class UserPlan(models.Model):
    """Links a user to their active subscription package."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_plan')
    package = models.ForeignKey(
        'packages.Package', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='subscribers'
    )
    is_active = models.BooleanField(default=True)
    activated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        pkg = self.package.name if self.package else 'No Package'
        return f"{self.user.username} — {pkg} ({'Active' if self.is_active else 'Inactive'})"


class Wallet(models.Model):
    """Wallet linked 1-to-1 with each User to track their balance."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet — ${self.balance}"

    def deposit(self, amount):
        """Add funds to the wallet and record a transaction."""
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        Transaction.objects.create(
            wallet=self,
            transaction_type='deposit',
            amount=amount,
            status='completed',
            note='Deposit to wallet',
        )
        # Note: self.balance is automatically recalculated by Transaction post_save signal
        self.refresh_from_db()
        return self.balance

    def withdraw(self, amount):
        """Deduct funds from the wallet and record a transaction."""
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        Transaction.objects.create(
            wallet=self,
            transaction_type='withdrawal',
            amount=amount,
            status='completed',
            note='Withdrawal from wallet',
        )
        # Note: self.balance is automatically recalculated by Transaction post_save signal
        self.refresh_from_db()
        return self.balance


class Earning(models.Model):
    """Credits earned by a user (e.g. from watching videos). Separate from Transaction."""
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='earnings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Earning +${self.amount} — {self.note[:50]}'


class Transaction(models.Model):
    """Ledger of all deposit and withdrawal transactions for a wallet."""
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    BANK_TYPE_CHOICES = (
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'Easypaisa'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    note = models.CharField(max_length=255, blank=True, default='')
    # Withdrawal request fields
    account_number = models.CharField(max_length=50, blank=True, default='')
    bank_type = models.CharField(max_length=20, choices=BANK_TYPE_CHOICES, blank=True, default='')
    bank_name = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type.title()} ${self.amount} — {self.status}"
