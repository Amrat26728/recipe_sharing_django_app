from django.db import models
from django.conf import settings
from accounts.models import User

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000, blank=True)
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    servings = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    chef_note = models.TextField(max_length=1000, blank=True)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_recipes', blank=True)


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.full_name} on {self.recipe.title}'