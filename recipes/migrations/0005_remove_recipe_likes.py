# Generated by Django 5.2.3 on 2025-06-12 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='likes',
        ),
    ]
