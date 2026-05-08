from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """Automatically create a Wallet with 0.00 balance when a new User registers."""
    if created:
        Wallet.objects.create(user=instance, balance=0.00)


@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    """Save the wallet whenever the user is saved (safety net)."""
    try:
        instance.wallet.save()
    except Wallet.DoesNotExist:
        Wallet.objects.create(user=instance, balance=0.00)
