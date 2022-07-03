from django.db import models
from django.contrib.postgres.fields import ArrayField
from . base import BaseUUIDTimeStampedModel
from . user import User


class Form(BaseUUIDTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True, null=True)
    is_live = models.BooleanField(default=True)
    elements = ArrayField(base_field=models.CharField(max_length=25), blank=True, null=True)

    class Meta:
        db_table = 'forms'

    def __str__(self) -> str:
        return self.title
