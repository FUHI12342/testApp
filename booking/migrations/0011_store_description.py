# Generated by Django 5.0.4 on 2024-06-20 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_remove_notice_content_notice_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='店舗情報'),
        ),
    ]
