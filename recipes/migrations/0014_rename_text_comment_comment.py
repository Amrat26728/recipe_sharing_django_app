# Generated by Django 5.2.3 on 2025-06-14 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
    ]
