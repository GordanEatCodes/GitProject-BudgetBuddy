from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'title',
            'rent',
            'location',
            'size',
            'has_internet',
            'has_private_bathroom',
            'near_station',
            'image',
            'available',
        ]
