# Generated by Django 4.2 on 2024-04-20 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_initialregistrationotp_otp_delete_otpverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialregistration',
            name='is_otp_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
