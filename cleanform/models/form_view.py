from django.db import models
from cleanform.models.base import BaseUUIDTimeStampedModel
from cleanform.models.form import Form


class FormView(BaseUUIDTimeStampedModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_views')
    ip_address = models.GenericIPAddressField()
    view_count = models.IntegerField(default=1)

    class Meta:
        db_table = 'form_views'
        unique_together = ['form', 'ip_address']
    
    def __str__(self) -> str:
        return self.ip_address