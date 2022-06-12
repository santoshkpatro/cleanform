from django.db import models
from django.contrib.postgres.fields import ArrayField
from . base import BaseUUIDModel
from . user import User


class Form(BaseUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_live = models.BooleanField(default=True)
    order = ArrayField(base_field=models.JSONField(), blank=True, null=True)

    class Meta:
        db_table = 'forms'
