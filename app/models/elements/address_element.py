from django.db import models
from ..base import BaseUUIDModel
from ..form import Form


class AddressElement(BaseUUIDModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_address_elements')
    label = models.CharField(max_length=200)
    is_required = models.BooleanField(default=False)

    # Visible Option
    is_street_visible = models.BooleanField(default=True)
    is_state_visible = models.BooleanField(default=True)
    is_country_visible = models.BooleanField(default=True)
    is_city_visible = models.BooleanField(default=True)

    # Sublabel
    state_sublabel = models.CharField(max_length=200, default='State')
    country_sublabel = models.CharField(max_length=200, default='Country')
    street_sublabel = models.CharField(max_length=200, default='Street Address')
    city_sublabel = models.CharField(max_length=200, default='City')

    # Other properties
    description = models.TextField(blank=True, null=True)
    input_field_font_size = models.IntegerField(blank=True, null=True)
    label_font_size = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'address_elements'
