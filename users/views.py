from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import (
    RegistrationForm, 
    RoleSelectForm, 
    OwnerMethodSelectForm, 
    TenantTypeSelectForm,
    TenantPreferenceForm,
)

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def home_view(request):
    profile = request.user.userprofile
    if profile.role == 'owner':
        return render(request, 'accounts/dashboard_owner.html')
    elif profile.role == 'coordinator':
        return render(request, 'accounts/dashboard_coordinator.html')
    else:
        return render(request, 'accounts/dashboard_tenant.html')
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('setup_role')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def setup_role_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = RoleSelectForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if profile.role == 'owner':
                return redirect('setup_owner_method')
            elif profile.role == 'tenant':
                return redirect('setup_tenant_type')
            else:
                return redirect('home')
    else:
        form = RoleSelectForm(instance=profile)
    return render(request, 'accounts/setup_role.html', {'form': form})

@login_required
def setup_owner_method_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = OwnerMethodSelectForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OwnerMethodSelectForm(instance=profile)
    return render(request, 'accounts/setup_owner_method.html', {'form': form})

@login_required
def setup_tenant_type_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = TenantTypeSelectForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TenantTypeSelectForm(instance=profile)
    return render(request, 'accounts/setup_tenant_type.html', {'form': form})

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

