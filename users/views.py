import random
from urllib import request
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from Budget_Buddy.settings import EMAIL_HOST_USER
from users.models import UserProfile
from .forms import (
    ForgotPasswordForm,
    ResetPasswordForm,
    LoginForm,
    ProfileSetupForm,
    RegistrationForm, 
    RoleSelectForm, 
    TenantPreferenceForm,
)
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about_us.html')

def about_dash(request):
    return render(request, 'about_us_dash.html')

@login_required
def dashboard(request):
    profile = request.user.userprofile
    
    name = profile.username.strip()
    if not name:
        name = request.user.first_name.strip()
    if not name:
        name = request.user.username.split('@')[0].strip()
    
    print(f"DEBUG - profile.username raw: '{profile.username}'")
    print(f"DEBUG - first_name raw: '{request.user.first_name}'")
    print(f"DEBUG - final name: '{name}'")
    
    return render(request, 'dashboard.html', {'display_name': name})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    if request.method == 'POST' and 'otp' in request.POST:
        entered = request.POST.get('otp', '').strip()
        saved = str(request.session.get('registration_otp'))
        data = request.session.get('registration_data', {})

        if entered == saved:
            user = User.objects.create_user( 
                username=data['email'],  # Use email as username for simplicity 
                email=data['email'], 
                password=data['password1']
            )
            user.first_name = data['fullname']
            user.save()
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
                from_email=None,  # Use default from_email from settings
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

        print(f"DEBUG - Entered OTP: '{entered}'")  # Debug entered OTP
        print(f"DEBUG - Saved OTP: '{saved}'")  # Debug saved OTP
        print(f"DEBUG - session keys: {list(request.session.keys())}")

        if entered == saved:
            if User.objects.filter(username=data['email']).exists():
                return render(request, 'accounts/register_otp.html', {
                    'email': data.get('email'),
                    'error': 'An account with this email already exists.'
                })
            
            user = User.objects.create_user(
                username=data['email'],  # Use email as username for simplicity
                email=data['email'], 
                password=data['password1']
            )
            user.first_name = data['fullname']
            user.save()
            login(request, user)
            
            try:
                del request.session['registration_otp']
            except KeyError:
                pass
            try:
                del request.session['registration_data']
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
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.authenticate_user()
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, 'Invalid credentials')

    return render(request, 'accounts/login.html', {'form': form}) 

def forgot_password_view(request):
    if request.method == 'POST': 
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = random.randint(100000, 999999)
            request.session['password_reset_otp'] = otp
            request.session['password_reset_email'] = email
            print(f"DEBUG - Password reset OTP: {otp}")  # Debug OTP
            send_mail(
                subject='Your OTP Code for Budget Buddy Password Reset',
                message=f'Your OTP code is: {otp}',
                from_email=None,
                recipient_list=[email],
            )
            return redirect('reset_password_otp')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})
        
def reset_password_otp_view(request):
    email = request.session.get('password_reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        entered = request.POST.get('otp', '').strip()
        saved = str(request.session.get('password_reset_otp',''))

        print(f"DEBUG - Entered OTP: '{entered}'")  # Debug entered OTP
        print(f"DEBUG - Saved OTP: '{saved}'")  # Debug saved OTP

        if entered == saved:
            return redirect('reset_password_new')
        else:
            return render(request, 'accounts/reset_password_otp.html', {
                'email': email,
                'error': 'Invalid OTP. Please try again.'
            })
    return render(request, 'accounts/reset_password_otp.html', {'email': email})

def reset_password_new_view(request):
    email = request.session.get('password_reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        print(f"DEBUG - POST data: {request.POST}")  # Debug POST data
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                for key in ['password_reset_otp', 'password_reset_email']:
                    request.session.pop(key, None)
                return redirect('login')
            except User.DoesNotExist:
                form.add_error(None, 'No account found with that email.')
    else:
        form = ResetPasswordForm()
    return render(request, 'accounts/reset_password_new.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about_us.html')


def contact(request):
    return render(request, 'contact_us.html')