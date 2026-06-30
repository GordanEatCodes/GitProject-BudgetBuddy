from django import forms
from .models import Room, Unit


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'title',
            'rent',

            'state',
            'city',
            'location_detail',

            'unit_type',
            'room_type',
            'floor_level',
            'bathroom_type',

            'near_mrt',
            'near_lrt',
            'near_ktm',
            'near_bus_stop',
            'near_train',
            'security_24h',
            'swimming_pool',
            'gym_room',
            'covered_carpark',
            'oku_friendly',
            'multi_purpose_hall',
            'playground',
            'has_surau',
            'near_mini_market',
            'co_living',
            'extra_parking',

            'has_aircond',
            'has_washing_machine',
            'has_wifi',
            'cooking_allowed',
            'has_tv',
            'shared_bathroom',
            'private_bathroom',
            'has_shower',

            'pet_allowed',
            'smoking_allowed',
            'prefer_zero_deposit',
            'prefer_move_in_immediately',
            'prefer_pet_allowed',
            'prefer_muslim_friendly',
            'prefer_smoking_allowed',

            'size',
            'image',
            'available',
        ]
        widgets = {
            'rent': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'size': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'floor_level': forms.NumberInput(attrs={'min': '0', 'placeholder': 'e.g., 0, 3, 15'}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'title',
            'rent',
            
            'state',
            'location_detail',
            
            'unit_type',
            'floor_level',
            'bedrooms',
            'bathrooms',

            'near_mrt',
            'near_lrt',
            'near_ktm',
            'near_bus_stop',
            'near_brt',
            'security_24h',
            'swimming_pool',
            'gym_room',
            'covered_carpark',
            'oku_friendly',
            'multi_purpose_hall',
            'playground',
            'near_mall',
            'near_shop_lots',
            'near_convenience_store',

            'has_aircond',
            'has_washing_machine',
            'has_wifi',
            'cooking_allowed',
            'shared_bathroom',
            'private_bathroom',
            'has_tv',
            'has_fridge',

            'pet_allowed',
            'smoking_allowed',

            'size',
            'image',
            'available',
        ]
        widgets = {
            'rent': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'size': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'floor_level': forms.NumberInput(attrs={'min': '0', 'placeholder': 'e.g., 0, 3, 15'}),
        }

