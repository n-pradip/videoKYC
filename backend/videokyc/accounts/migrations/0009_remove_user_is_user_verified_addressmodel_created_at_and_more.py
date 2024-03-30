# Generated by Django 4.2 on 2024-03-30 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_is_phone_verified_user_user_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_user_verified',
        ),
        migrations.AddField(
            model_name='addressmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='addressmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
