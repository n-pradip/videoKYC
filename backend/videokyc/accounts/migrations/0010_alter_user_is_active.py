# Generated by Django 4.2 on 2024-03-30 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_user_is_user_verified_addressmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
