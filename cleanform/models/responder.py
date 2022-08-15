from django.db import models
from cleanform.models.base import BaseUUIDTimeStampedModel
from .email_service import EmailService
from cleanform.models.form import Form


class Responder(BaseUUIDTimeStampedModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_responders')
    email_service = models.ForeignKey(EmailService, on_delete=models.SET_NULL, null=True, blank=True, related_name='email_service_responders')
    email = models.EmailField(max_length=255)
    subject = models.TextField()
    description = models.TextField()
    target_email_label = models.CharField(max_length=100, default='email')

    class Meta:
        db_table = 'responders'

    def __str__(self) -> str:
        return str(self.id)