import profile
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from .forms import (
    LoginForm,
    ProfileSetupForm,
    RegistrationForm, 
    RoleSelectForm, 
    TenantPreferenceForm,
)

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("Form errors:", form.errors)  # Debugging line to print form errors
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('setup_role')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def setup_role_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = RoleSelectForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.refresh_from_db()  # Refresh to get updated role
            if profile.role == 'tenant':
                return redirect('setup_profile')
            elif profile.role == 'owner':
                return redirect('setup_profile')
            else:
                return redirect('home')
    else:
        form = RoleSelectForm(instance=profile)
    return render(request, 'accounts/setup_role.html', {'form': form})

@login_required
def setup_profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if profile.role == 'tenant':
                return redirect('setup_tenant_preferences')
            else:
                return redirect('home')
    else:
        form = ProfileSetupForm(instance=profile)
    return render(request, 'accounts/setup_profile.html', {'form': form})

@login_required
def setup_tenant_preferences_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = TenantPreferenceForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TenantPreferenceForm(instance=profile)
    return render(request, 'accounts/setup_tenant_preferences.html', {'form': form})

@login_required
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            from django.contrib.auth import authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


