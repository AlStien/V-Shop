# Generated by Django 3.2.8 on 2021-11-01 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='otp_email',
            new_name='otp',
        ),
    ]
