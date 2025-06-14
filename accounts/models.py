from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, default=None)
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=1000, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
