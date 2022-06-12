from rest_framework import serializers
from tzapp.models.elements.name_element import NameElement
from tzapp.models.elements.address_element import AddressElement


class NameElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameElement
        fields = [
            'id',
            'label',
            'is_required',
            'is_first_name_visible',
            'is_middle_name_visible',
            'is_last_name_visible',
            'first_name_sublabel',
            'middle_name_sublabel',
            'last_name_sublabel',
            'first_name_placeholder',
            'middle_name_placeholder',
            'last_name_placeholder',
            'description',
            'input_field_font_size',
            'label_font_size',
        ]


class AddressElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressElement
        fields = [
            'id',
            'label',
            'is_required',
            'is_street_visible',
            'is_state_visible',
            'is_country_visible',
            'is_city_visible',
            'state_sublabel',
            'country_sublabel',
            'street_sublabel',
            'city_sublabel',
            'description',
            'input_field_font_size',
            'label_font_size',
        ]
