from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .base import BaseUUIDModel


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not full_name:
            raise ValueError('Users must have an full name')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(BaseUUIDModel, AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)

    google_id = models.CharField(max_length=200, blank=True, null=True)
    github_id = models.CharField(max_length=200, blank=True, null=True)

    password_reset_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        ordering = ('email',)
        db_table = 'users'

    def __str__(self) -> str:
        return self.email

    def avatar_url(self):
        if not self.avatar:
            return None

        return "assets.app.com/%s".format(self.avatar)

    """Admin panel config"""

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
