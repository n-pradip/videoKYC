# Generated by Django 4.2 on 2024-03-27 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_user_is_email_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='initial_registration_attributes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.initialregistration'),
        ),
    ]
