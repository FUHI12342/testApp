# Generated by Django 5.0.4 on 2024-08-13 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0014_remove_customer_line_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_name',
            field=models.CharField(default='default name', max_length=255),
        ),
    ]
