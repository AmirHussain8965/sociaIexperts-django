from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Wallet, Transaction, Earning, ReferralProfile


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """Automatically create a Wallet and ReferralProfile when a new User registers."""
    if created:
        Wallet.objects.create(user=instance, balance=0.00)
        ReferralProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    """Save the wallet whenever the user is saved (safety net)."""
    try:
        instance.wallet.save()
    except Wallet.DoesNotExist:
        Wallet.objects.create(user=instance, balance=0.00)


def recalculate_wallet_balance(wallet):
    """
    Recalculate wallet balance from scratch.
    Balance = completed Transaction deposits + Earnings - completed Transaction withdrawals
    """
    stats = wallet.transactions.aggregate(
        total_deposits=Sum('amount', filter=Q(transaction_type='deposit', status='completed')),
        total_withdrawals=Sum('amount', filter=Q(transaction_type='withdrawal', status='completed'))
    )
    total_deposits = stats['total_deposits'] or Decimal('0.00')
    total_withdrawals = stats['total_withdrawals'] or Decimal('0.00')
    total_earnings = wallet.earnings.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    wallet.balance = total_deposits + total_earnings - total_withdrawals
    wallet.save(update_fields=['balance'])


@receiver(post_save, sender=Transaction)
def update_balance_on_transaction_save(sender, instance, **kwargs):
    """Update wallet balance when a transaction is saved."""
    if instance.wallet:
        recalculate_wallet_balance(instance.wallet)


@receiver(post_delete, sender=Transaction)
def update_balance_on_transaction_delete(sender, instance, **kwargs):
    """Update wallet balance when a transaction is deleted."""
    if instance.wallet:
        recalculate_wallet_balance(instance.wallet)


@receiver(post_save, sender=Earning)
def update_balance_on_earning_save(sender, instance, **kwargs):
    """Update wallet balance when an earning is created."""
    if instance.wallet:
        recalculate_wallet_balance(instance.wallet)


@receiver(post_delete, sender=Earning)
def update_balance_on_earning_delete(sender, instance, **kwargs):
    """Update wallet balance when an earning is deleted."""
    if instance.wallet:
        recalculate_wallet_balance(instance.wallet)

