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
    """Login form that accepts username or email and password.

    Methods:
    - authenticate_user(): returns authenticated User or None
    - get_user_profile(): returns related UserProfile or None
    """

    username_or_email = forms.CharField(label='Username or Email', max_length=254, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned = super().clean()
        username_or_email = cleaned.get('username_or_email')
        password = cleaned.get('password')

        if username_or_email and password:
            # Try to find user by username first, then by email
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    user = None

            if user is None:
                raise forms.ValidationError('Invalid username/email or password')

            # check password
            if not user.check_password(password):
                raise forms.ValidationError('Invalid username/email or password')

            # attach the authenticated user to the form instance
            self.user = user

        return cleaned

    def authenticate_user(self):
        """Return the authenticated User or None. Call after is_valid()."""
        return getattr(self, 'user', None)

    def get_user_profile(self):
        """Return related UserProfile instance if available, else None."""
        user = self.authenticate_user()
        if not user:
            return None
        try:
            return user.userprofile
        except Exception:
            return None

