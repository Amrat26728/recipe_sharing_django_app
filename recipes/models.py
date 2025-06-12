from django.db import models
from django.conf import settings
from accounts.models import User

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    servings = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    chef_note = models.TextField(max_length=1000)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    posted_at = models.DateTimeField(auto_now_add=True)