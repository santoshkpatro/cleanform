from django.db import models
from cleanform.models.form import Form
from nanoid import generate


class Element(models.Model):
    ELEMENT_TYPE_CHOICES = (
        ('page_break', 'page_break'),
        ('input_field', 'input_field'),
        ('checkbox_field', 'checkbox_field'),
        ('radio_field', 'radio_field')
    )
    
    id = models.CharField(max_length=25, primary_key=True, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_elements')
    label = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_required = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=ELEMENT_TYPE_CHOICES)
    properties = models.JSONField(blank=True, null=True)
    layouts = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'elements'

    def __str__(self) -> str:
        return self.label

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate()
        return super().save(*args, **kwargs)