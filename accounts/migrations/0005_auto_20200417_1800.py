# Generated by Django 3.0.1 on 2020-04-17 12:30

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, unique=True, upload_to=accounts.models.upload_profile_image),
        ),
    ]
