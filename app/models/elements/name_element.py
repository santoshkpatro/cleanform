from django.db import models
from ..base import BaseUUIDModel
from ..form import Form


class NameElement(BaseUUIDModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_name_elements')
    label = models.CharField(max_length=200)
    is_required = models.BooleanField(default=False)

    # Visible Option
    is_first_name_visible = models.BooleanField(default=True)
    is_middle_name_visible = models.BooleanField(default=True)
    is_last_name_visible = models.BooleanField(default=True)

    # Sublabel
    first_name_sublabel = models.CharField(max_length=200, default='First Name')
    middle_name_sublabel = models.CharField(max_length=200, default='Middle Name')
    last_name_sublabel = models.CharField(max_length=200, default='Last Name')

    # Placeholder
    first_name_placeholder = models.CharField(max_length=200, default="")
    middle_name_placeholder = models.CharField(max_length=200, default="")
    last_name_placeholder = models.CharField(max_length=200, default="")

    # Other properties
    description = models.TextField(blank=True, null=True)
    input_field_font_size = models.IntegerField(blank=True, null=True)
    label_font_size = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'name_elements'
