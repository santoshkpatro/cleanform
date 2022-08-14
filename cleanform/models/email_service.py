from django.db import models
from django.conf import settings
from cleanform.models.base import BaseUUIDTimeStampedModel
from cleanform.models.user import User
from cryptography.fernet import Fernet


class EmailService(BaseUUIDTimeStampedModel):
    TYPE_CHOICES = (
        ('SMTP', 'SMTP'),
        ('SDK', 'SDK')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_email_services')
    type = models.CharField(default='SMTP', choices=TYPE_CHOICES, max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # Email SMTP Configuration
    host = models.CharField(max_length=100)
    port = models.CharField(max_length=10)
    tls_enabled = models.BooleanField(default=True)

    # Encrypted Fields
    _host_user = models.CharField(max_length=100, db_column='host_user')
    _host_password = models.CharField(max_length=100, db_column='host_password')

    class Meta:
        db_table = 'email_services'

    def set_host_user(self, new_host_user):
        new_host_user_token = Fernet(settings.FERNET_KEY).encrypt(new_host_user.encode('utf-8'))
        self._host_user = new_host_user_token.decode('utf-8')

    def set_host_password(self, new_host_password):
        new_host_password_token = Fernet(settings.FERNET_KEY).encrypt(new_host_password.encode('utf-8'))
        self._host_password = new_host_password_token.decode('utf-8')

    @property
    def host_user(self):
        host_user_token = Fernet(bytes(settings.FERNET_KEY, 'utf-8')).decrypt(self._host_user.encode('utf-8'))
        return host_user_token.decode('utf-8')

    @property
    def host_password(self):
        host_password_token = Fernet(bytes(settings.FERNET_KEY, 'utf-8')).decrypt(self._host_password.encode('utf-8'))
        return host_password_token.decode('utf-8')

    def __str__(self) -> str:
        return str(self.id)

