# Generated by Django 5.2.2 on 2025-06-11 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='note',
        ),
    ]
