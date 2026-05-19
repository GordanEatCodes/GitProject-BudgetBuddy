import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
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
    if request.user.is_authenticated:
        return redirect('dashboard') 
    if request.method == 'POST' and 'otp' in request.POST:
        entered = request.POST.get('otp', '').strip()
        saved = str(request.session.get('registration_otp'))
        data = request.session.get('registration_data', {})

        if entered == saved:
            user = User.objects.create_user(
                username=data['fullname'], 
                email=data['email'], 
                password=data['password1']
            )
            login(request, user)
            del request.session['registration_otp']
            del request.session['registration_data']
            return redirect('setup_role')
        else:
            return render(request, 'accounts/register_otp.html', {
                'email': data.get('email'),
                'error': 'Invalid OTP. Please try again.'
            })
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000, 999999)
            request.session['registration_otp'] = otp
            request.session['registration_data'] = {
                'fullname': form.cleaned_data['fullname'],
                'email': form.cleaned_data['email'],
                'password1': form.cleaned_data['password1'],
            }
            print(f"DEBUG - OTP is: {otp}")  # For testing purposes, print OTP to console
            print(f"DEBUG - Sending OTP to: {form.cleaned_data['email']}")  # Debug email
            send_mail(
                subject='Your OTP Code for Budget Buddy Registration',
                message=f'Your OTP code is: {otp}',
                from_email='gordan.ng.hungzhuen@student.mmu.edu.my',
                recipient_list=[form.cleaned_data['email']],
            )
            print("DEBUG - Email sent")  # Debug email sent
            return redirect('register_otp')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'stage': 'form'
    })

def register_otp_view(request):
    data = request.session.get('registration_data', {})
    if not data:
        return redirect('register')
    
    if request.method == 'POST':
        entered = request.POST.get('otp', '').strip()
        saved = str(request.session.get('registration_otp',''))

        if entered == saved:
            user = User.objects.create_user(
                username=data['fullname'], 
                email=data['email'], 
                password=data['password1']
            )
            login(request, user)
            try:
                del request.session['registration_otp']
            except KeyError:
                pass
            try:
                del request.session['registration_data', None]
            except KeyError:
                pass
            return redirect('setup_role')
        else:
            return render(request, 'accounts/register_otp.html', {
                'email': data.get('email'),
                'error': 'Invalid OTP. Please try again.'
            })
    return render(request, 'accounts/register_otp.html', {
        'email': data.get('email')
    })



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
                return redirect('dashboard')
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
            return redirect('dashboard')
    else:
        form = TenantPreferenceForm(instance=profile)
    return render(request, 'accounts/setup_tenant_preferences.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['username'] 
            password1 = form.cleaned_data['password1']
            from django.contrib.auth import authenticate
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


