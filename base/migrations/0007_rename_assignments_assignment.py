# Generated by Django 4.2 on 2023-04-30 17:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_assignments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Assignments',
            new_name='Assignment',
        ),
    ]
