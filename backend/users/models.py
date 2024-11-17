from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
