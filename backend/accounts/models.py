from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A user who logs in with email instead of a separate username."""
    username = None
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
