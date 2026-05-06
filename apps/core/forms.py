from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your mail',
                'class': 'form-control',
                'aria-label': 'Email',
            })
        }
