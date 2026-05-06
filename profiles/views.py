from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def dashboard_view(request):
    """User dashboard view"""
    context = {'user_data': request.user}
    return render(request, 'profiles/dashboard.html', context)

@login_required(login_url='accounts:login')
def profile_view(request):
    """User profile view"""
    context = {'user_data': request.user}
    return render(request, 'profiles/profile.html', context)
