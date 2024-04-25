# Generated by Django 5.0.1 on 2024-04-12 04:51

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_user_id', models.CharField(max_length=255, verbose_name='LINEユーザーID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='名前')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='店名')),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255, unique=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='表示名')),
                ('line_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='LINE ID')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/', verbose_name='サムネイル画像')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='自己紹介文')),
                ('price', models.IntegerField(default=0, verbose_name='価格')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.store', verbose_name='店舗')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_number', models.CharField(default=uuid.uuid4, editable=False, max_length=255, verbose_name='予約番号')),
                ('start', models.DateTimeField(verbose_name='開始時間')),
                ('end', models.DateTimeField(verbose_name='終了時間')),
                ('is_temporary', models.BooleanField(default=True, verbose_name='仮予約フラグ')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.customer', verbose_name='顧客')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.staff', verbose_name='占いスタッフ')),
            ],
        ),
    ]
