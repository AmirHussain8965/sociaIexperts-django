from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum, Count, Q
from .models import Wallet, Transaction

BANK_TYPE_LABELS = dict(Transaction.BANK_TYPE_CHOICES)


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
        total_withdrawals=Sum('amount', filter=Q(transaction_type='withdrawal', status='completed')),
        transaction_count=Count('id'),
    )

    total_earnings = wallet.earnings.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    recent_transactions = wallet.transactions.all()[:10]

    context = {
        'user_data': request.user,
        'wallet': wallet,
        'total_earnings': total_earnings,
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
    """Handle withdrawal requests — creates a pending transaction for admin approval."""
    wallet = _get_wallet(request.user)

    # Pending withdrawals lock that balance until approved/rejected
    pending_amount = wallet.transactions.filter(
        transaction_type='withdrawal', status='pending'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    available_balance = wallet.balance - pending_amount

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            account_number = request.POST.get('account_number', '').strip()
            bank_type = request.POST.get('bank_type', '').strip()
            bank_name = request.POST.get('bank_name', '').strip()

            if amount <= 0:
                messages.error(request, 'Please enter a valid amount greater than zero.')
            elif amount < Decimal('10.00'):
                messages.error(request, 'Minimum withdrawal amount is $10.00.')
            elif amount > available_balance:
                messages.error(
                    request,
                    f'Insufficient available balance. Available: ${available_balance:.2f}'
                    + (f' (${pending_amount:.2f} pending)' if pending_amount > 0 else '') + '.'
                )
            elif not account_number:
                messages.error(request, 'Please enter your account / IBAN number.')
            elif not bank_type:
                messages.error(request, 'Please select a payment method.')
            elif bank_type == 'other' and not bank_name:
                messages.error(request, 'Please specify your bank / service name.')
            else:
                display_bank = bank_name if bank_type == 'other' else BANK_TYPE_LABELS.get(bank_type, bank_type)
                note = f'Withdrawal via {display_bank} — A/C: {account_number}'

                Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='withdrawal',
                    amount=amount,
                    status='pending',
                    account_number=account_number,
                    bank_type=bank_type,
                    bank_name=bank_name if bank_type == 'other' else '',
                    note=note,
                )
                messages.success(
                    request,
                    f'Withdrawal request of ${amount:.2f} submitted successfully. '
                    'It will be processed once approved by an admin.'
                )
                return redirect('profiles:dashboard')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, str(e) if str(e) != '' else 'Invalid amount entered.')

    context = {
        'wallet': wallet,
        'available_balance': available_balance,
        'pending_amount': pending_amount,
        'user_data': request.user,
        'bank_type_choices': Transaction.BANK_TYPE_CHOICES,
    }
    return render(request, 'profiles/withdraw.html', context)


@login_required(login_url='accounts:login')
def plans_view(request):
    """Show all available packages; highlight the user's active plan."""
    from apps.packages.models import Package
    from .models import UserPlan
    packages = Package.objects.prefetch_related('features').all()
    try:
        user_plan = request.user.user_plan if request.user.user_plan.is_active else None
    except UserPlan.DoesNotExist:
        user_plan = None
    context = {
        'packages': packages,
        'user_plan': user_plan,
        'user_data': request.user,
    }
    return render(request, 'profiles/plans.html', context)


@login_required(login_url='accounts:login')
def profile_view(request):
    """User profile view — includes referral code and stats."""
    from .models import ReferralProfile, ReferralBonus
    referral_profile, _ = ReferralProfile.objects.get_or_create(user=request.user)
    bonus = ReferralBonus.load()
    context = {
        'user_data': request.user,
        'referral_profile': referral_profile,
        'referral_bonus': bonus.amount,
    }
    return render(request, 'profiles/profile.html', context)
