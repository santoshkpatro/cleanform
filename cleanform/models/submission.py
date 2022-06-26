from django.db import models
from . base import BaseUUIDTimeStampedModel
from . form import Form


class Submission(BaseUUIDTimeStampedModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='form_submissions')
    data = models.JSONField()
    is_spam = models.BooleanField(default=False)

    class Meta:
        db_table = 'submissions'

    def __str__(self) -> str:
        return str(self.id)
