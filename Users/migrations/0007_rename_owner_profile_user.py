# Generated by Django 4.2.5 on 2023-09-22 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_rename_user_profile_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='owner',
            new_name='user',
        ),
    ]
