import random
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import OTPRecord
@require_http_methods(['GET', 'POST'])
@csrf_protect
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@require_http_methods(['GET', 'POST'])
@csrf_protect
def register_view(request):
    """User registration view — handles both master code and referral code signups."""
    if request.user.is_authenticated:
        return redirect('core:home')

    # Pre-fill referral code from ?ref= query param
    ref_code = request.GET.get('ref', '')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            # Credit referral bonus if a user referral code was used
            referrer = getattr(form, 'referrer', None)
            if referrer:
                from decimal import Decimal
                from profiles.models import ReferralBonus, ReferralRecord, Wallet, Earning
                bonus = ReferralBonus.load()
                if bonus.amount > 0:
                    ReferralRecord.objects.create(
                        referrer=referrer,
                        referred=user,
                        reward_amount=bonus.amount,
                    )
                    wallet, _ = Wallet.objects.get_or_create(
                        user=referrer,
                        defaults={'balance': Decimal('0.00')}
                    )
                    Earning.objects.create(
                        wallet=wallet,
                        amount=bonus.amount,
                        note=f'Referral bonus — {user.username} joined using your code',
                    )

            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        initial = {'referral_code': ref_code} if ref_code else {}
        form = RegisterForm(initial=initial)

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='accounts:login')
def logout_view(request):
    """User logout view"""
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('accounts:login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:register')

@require_http_methods(['GET', 'POST'])
@csrf_protect
def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            
            # Save or update OTP Record
            OTPRecord.objects.update_or_create(
                user=user,
                defaults={'otp_code': otp_code, 'created_at': timezone.now()}
            )
            
            # Send Email
            mail_subject = 'Password Reset OTP'
            message = f"Hi {user.username},\n\nYour 6-digit OTP for password reset is: {otp_code}\n\nThis OTP is valid for 10 minutes."
            email_msg = EmailMessage(mail_subject, message, to=[email])
            email_msg.send()
            
            request.session['reset_email'] = email
            messages.info(request, 'An OTP has been sent to your email.')
            return redirect('accounts:verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            
    return render(request, 'accounts/forgot_password.html')

@require_http_methods(['GET', 'POST'])
@csrf_protect
def verify_otp_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
        
    email = request.session.get('reset_email')
    if not email:
        return redirect('accounts:forgot_password')
        
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        try:
            user = User.objects.get(email=email)
            otp_record = OTPRecord.objects.get(user=user, otp_code=otp_code)
            
            # Check if OTP is within 10 minutes
            time_difference = timezone.now() - otp_record.created_at
            if time_difference > timedelta(minutes=10):
                otp_record.delete()
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('accounts:forgot_password')
                
            # Valid OTP
            otp_record.delete()
            request.session['otp_verified'] = True
            return redirect('accounts:reset_password')
            
        except (User.DoesNotExist, OTPRecord.DoesNotExist):
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'accounts/verify_otp.html')

@require_http_methods(['GET', 'POST'])
@csrf_protect
def reset_password_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if not request.session.get('otp_verified'):
        return redirect('accounts:forgot_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            email = request.session.get('reset_email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                
                # Clear session
                del request.session['reset_email']
                del request.session['otp_verified']
                
                messages.success(request, 'Password reset successfully. You can now login.')
                return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                
    return render(request, 'accounts/reset_password.html')
