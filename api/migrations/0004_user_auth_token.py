# Generated by Django 5.0.1 on 2024-01-17 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_photo_url_user_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_token',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
