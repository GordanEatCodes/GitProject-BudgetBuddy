from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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

class OwnerMethodSelectForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['rental_method']

class TenantTypeSelectForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tenant_type']

class TenantPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'gender',   
            'sleep_schedule',
            'cleanliness',
            'noise_tolerance',
            'religion',
            'study_habits',
        ]