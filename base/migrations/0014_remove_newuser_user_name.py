# Generated by Django 3.2.8 on 2021-11-01 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_newuser_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='user_name',
        ),
    ]
