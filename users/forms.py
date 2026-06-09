from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    fullname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True, help_text=" Your password must be at least 8 characters long and contain a mix of letters and numbers.")
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True, help_text=" Enter the same password again. ")
    
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    
class RoleSelectForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'phone_number',
            'bio',
            'state',
        ]
        widgets = {
             'username': forms.TextInput(attrs={
                'placeholder': 'How should we call you?',
                'autocomplete': 'nickname',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+60 12-345 6789',
                'autocomplete': 'tel',
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell owners or tenants a bit about yourself…',
                'rows': 4,
            }),
        }

class TenantPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'gender',   
            'sleep_schedule',
            'cleanliness',
            'noise_tolerance',
            'race',
            'religion',
            'study_habits',
        ]

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=254, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned = super().clean()
        username_or_email = cleaned.get('username_or_email')
        password = cleaned.get('password')

        if username_or_email and password:
            user = None

            # 1. Try Django User.username
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                pass

            # 2. Try User.email
            if user is None:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    pass

            # 3. Try UserProfile.username  ← NEW: this is what was missing
            if user is None:
                try:
                    profile = UserProfile.objects.get(username=username_or_email)
                    user = profile.user
                except UserProfile.DoesNotExist:
                    pass

            if user is None or not user.check_password(password):
                raise forms.ValidationError('Invalid username/email or password.')

            self.user = user

        return cleaned

    def authenticate_user(self):
        return getattr(self, 'user', None)

    def get_user_profile(self):
        user = self.authenticate_user()
        if not user:
            return None
        try:
            return user.userprofile   # ← FIX: was user.UserProfile (capital U breaks the reverse relation)
        except Exception:
            return None