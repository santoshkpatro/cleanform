from django.db import models
from cleanform.models.base import BaseUUIDTimeStampedModel
from cleanform.models.responder import Responder


class ResponderLog(BaseUUIDTimeStampedModel):
    responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name='responder_logs')
    info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'responder_logs'

    def __str__(self) -> str:
        return str(self.id)