# Generated by Django 3.0.1 on 2019-12-27 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('phone_no', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=8)),
                ('password', models.CharField(max_length=20)),
                ('confirm_password', models.CharField(max_length=20)),
            ],
        ),
    ]