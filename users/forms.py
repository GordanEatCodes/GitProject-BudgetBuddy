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
            'Username',
            'phone_number',
            'bio',
            'state',
        ]
        widgets = {
             'Username': forms.TextInput(attrs={
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
    username = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
