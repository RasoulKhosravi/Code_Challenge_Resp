# Generated by Django 4.2.7 on 2024-12-15 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='owner',
            new_name='user',
        ),
    ]
