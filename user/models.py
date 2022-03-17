import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model, using email as username
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None
    objects = CustomUserManager()

    # Replace the ID field with a UUID for better security
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"]),
        ]
