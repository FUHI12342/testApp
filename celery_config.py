from __future__ import absolute_import, unicode_literals
from celery import Celery
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

print('Before autodiscover_tasks:', app)
app.autodiscover_tasks()
print('After autodiscover_tasks:', app)

print('celery_config.py終了')
