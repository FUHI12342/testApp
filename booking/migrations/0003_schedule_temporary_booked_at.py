# Generated by Django 5.0.1 on 2024-04-18 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_schedule_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='temporary_booked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
