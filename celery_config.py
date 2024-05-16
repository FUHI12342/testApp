from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Djangoの設定をロード
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()  # Djangoの設定をロード

from django.conf import settings  # Djangoの設定をインポート

print('celery_config.py')
app = Celery('booking')

# 'project.settings'から設定を読み込む
app.config_from_object('project.settings', namespace='CELERY')

# Beatスケジューラの設定
app.conf.beat_schedule = {
    'delete-every-minute': {
        'task': 'booking.views.delete_temporary_schedules',  # タスクの場所を指定
        'schedule': 60.0,  # 60秒ごとに実行
    },
}

# booking.viewsを明示的にインポート
import booking.views  # これが重要です

print('Before autodiscover_tasks:', app)
app.autodiscover_tasks()
print('After autodiscover_tasks:', app)

print('celery_config.py終了')
