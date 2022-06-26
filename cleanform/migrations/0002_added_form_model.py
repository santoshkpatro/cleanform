# Generated by Django 4.0.5 on 2022-06-25 14:44

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cleanform', '0001_added_user_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=300, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_live', models.BooleanField(default=True)),
                ('order', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, null=True, size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'forms',
            },
        ),
    ]