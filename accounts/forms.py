from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    """Login form inheriting from AuthenticationForm"""
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter user name or email',
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })


class RegisterForm(UserCreationForm):
    """User registration form inheriting from UserCreationForm"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': 'form-control'
        })
    )
    referral_code = forms.CharField(
        required=True,
        label='Registration / Referral Code',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter master code or a friend\'s referral code',
            'class': 'form-control'
        })
    )


    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'class': 'form-control'
        })
        # UserCreationForm uses password1 and password2
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })

    def clean_referral_code(self):
        code = self.cleaned_data.get('referral_code', '').strip()
        from .models import MasterSignupCode
        from profiles.models import ReferralProfile

        master = MasterSignupCode.load()
        if not master:
            raise forms.ValidationError("Registration is currently disabled.")

        # 1. Accept the global master code (no referrer)
        if code == master.code:
            self.referrer = None
            return code

        # 2. Accept a valid user referral code
        try:
            rp = ReferralProfile.objects.select_related('user').get(code=code.upper())
            self.referrer = rp.user
            return code.upper()
        except ReferralProfile.DoesNotExist:
            pass

        raise forms.ValidationError("Invalid registration or referral code.")
