from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


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
        self.balance += amount
        self.save()
        Transaction.objects.create(
            wallet=self,
            transaction_type='deposit',
            amount=amount,
            status='completed',
            note='Deposit to wallet',
        )
        return self.balance

    def withdraw(self, amount):
        """Deduct funds from the wallet and record a transaction."""
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(
            wallet=self,
            transaction_type='withdrawal',
            amount=amount,
            status='completed',
            note='Withdrawal from wallet',
        )
        return self.balance


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

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    note = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type.title()} ${self.amount} — {self.status}"
