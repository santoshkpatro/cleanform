import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleanform.settings.development')

app = Celery('cleanform')
app.config_from_object('django.conf:settings', namespace='CELERY')
