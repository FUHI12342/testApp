# Generated by Django 5.0.4 on 2024-08-14 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_rename_customer_schedule_customer_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer_name',
            new_name='full_name',
        ),
    ]