# Generated by Django 5.0.1 on 2024-01-14 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]
