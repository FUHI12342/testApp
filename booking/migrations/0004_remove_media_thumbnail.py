# Generated by Django 5.0.4 on 2024-06-18 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_media_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='thumbnail',
        ),
    ]
