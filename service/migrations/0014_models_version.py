# Generated by Django 3.2.23 on 2024-01-29 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_auto_20240113_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='models',
            name='version',
            field=models.JSONField(blank=True, null=True),
        ),
    ]