# Generated by Django 5.0.4 on 2024-08-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_remove_customer_name_customer_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='customer',
            new_name='customer_name',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_name',
            field=models.CharField(max_length=255),
        ),
    ]