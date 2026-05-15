from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import NewsletterForm
from .models import Newsletter
from apps.packages.models import Package


def home(request):
    """Home page view"""
    return render(request, 'index.html')


def about(request):
    """About page view"""
    return render(request, 'about.html')


def services(request):
    """Services page view"""
    packages = Package.objects.all().prefetch_related('features')
    return render(request, 'services.html', {'packages': packages})


def projects(request):
    """Projects page view"""
    return render(request, 'projects.html')


def blog(request):
    """Blog page view"""
    return render(request, 'blog.html')


@require_http_methods(['POST'])
@csrf_protect
def newsletter_subscribe(request):
    """Newsletter subscription view"""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        try:
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                if newsletter.is_active:
                    messages.info(request, 'You are already subscribed.')
                else:
                    newsletter.is_active = True
                    newsletter.save()
                    messages.success(request, 'Successfully subscribed to our newsletter!')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        messages.error(request, 'Invalid email address.')

    return redirect(request.POST.get('next', 'core:home'))
