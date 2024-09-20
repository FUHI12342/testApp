# Generated by Django 5.0.4 on 2024-08-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_schedule_memo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='line_user_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='hashed_line_user_id',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]