from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum, Count, Q
from .models import Wallet, Transaction


def _get_wallet(user):
    """Get or create a wallet for the given user."""
    wallet, _ = Wallet.objects.get_or_create(
        user=user,
        defaults={'balance': Decimal('0.00')}
    )
    return wallet


@login_required(login_url='accounts:login')
def dashboard_view(request):
    """User dashboard view — fetches wallet, stats, and recent transactions."""
    wallet = _get_wallet(request.user)

    # Aggregate stats from transactions
    stats = wallet.transactions.aggregate(
        total_deposits=Sum('amount', filter=Q(transaction_type='deposit', status='completed')),
        total_withdrawals=Sum('amount', filter=Q(transaction_type='withdrawal', status='completed')),
        transaction_count=Count('id'),
    )

    recent_transactions = wallet.transactions.all()[:10]

    context = {
        'user_data': request.user,
        'wallet': wallet,
        'total_deposits': stats['total_deposits'] or Decimal('0.00'),
        'total_withdrawals': stats['total_withdrawals'] or Decimal('0.00'),
        'transaction_count': stats['transaction_count'] or 0,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'profiles/dashboard.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def deposit_view(request):
    """Handle deposits into the user's wallet."""
    wallet = _get_wallet(request.user)

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount <= 0:
                messages.error(request, 'Please enter a valid amount greater than zero.')
            else:
                wallet.deposit(amount)
                messages.success(request, f'${amount:.2f} deposited successfully!')
                return redirect('profiles:dashboard')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, str(e) if str(e) != '' else 'Invalid amount entered.')

    context = {
        'wallet': wallet,
        'user_data': request.user,
    }
    return render(request, 'profiles/deposit.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def withdraw_view(request):
    """Handle withdrawals from the user's wallet."""
    wallet = _get_wallet(request.user)

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount <= 0:
                messages.error(request, 'Please enter a valid amount greater than zero.')
            elif amount > wallet.balance:
                messages.error(request, 'Insufficient balance for this withdrawal.')
            else:
                wallet.withdraw(amount)
                messages.success(request, f'${amount:.2f} withdrawn successfully!')
                return redirect('profiles:dashboard')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, str(e) if str(e) != '' else 'Invalid amount entered.')

    context = {
        'wallet': wallet,
        'user_data': request.user,
    }
    return render(request, 'profiles/withdraw.html', context)


@login_required(login_url='accounts:login')
def profile_view(request):
    """User profile view"""
    context = {'user_data': request.user}
    return render(request, 'profiles/profile.html', context)
