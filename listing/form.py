from django import forms
from .models import Room, Unit


from django import forms
from .models import Room, Unit

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'title',
            'rent',
            'state',
            'location_detail',
            'unit_type',
            'floor_level',
            'bathroom_type',

            # strategies
            'near_mrt',
            'near_lrt',
            'near_ktm',
            'near_bus_stop',
            'near_brt',
            'security_24h',
            'swimming_pool',
            'gym_room',
            'covered_carpark',
            'near_mall',
            'near_shop_lots',
            'near_convenience_store',

            # utilities
            'has_aircond',
            'has_washing_machine',
            'has_wifi',
            'cooking_allowed',
            'shared_bathroom',
            'private_bathroom',
            'has_tv',
            'has_fridge',

            # flexibility
            'pet_allowed',
            'smoking_allowed',

            'size',
            'image',
            'available',
        ]


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

            # strategies
            'near_mrt',
            'near_lrt',
            'near_ktm',
            'near_bus_stop',
            'near_brt',
            'security_24h',
            'swimming_pool',
            'gym_room',
            'covered_carpark',
            'near_mall',
            'near_shop_lots',
            'near_convenience_store',

            # utilities
            'has_aircond',
            'has_washing_machine',
            'has_wifi',
            'cooking_allowed',
            'shared_bathroom',
            'private_bathroom',
            'has_tv',
            'has_fridge',

            # flexibility
            'pet_allowed',
            'smoking_allowed',

            'size',
            'image',
            'available',
        ]
