from __future__ import absolute_import, unicode_literals
from celery import Celery
print('celery_config.py')
app = Celery('booking')

# 'project.settings'から設定を読み込む
app.config_from_object('project.settings', namespace='CELERY')

# 非推奨の設定を新しいものに更新
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.broker_connection_retry_on_startup = True

# Beatスケジューラの設定
app.conf.beat_schedule = {
    'delete-every-minute': {
        'task': 'booking.views.delete_temporary_schedules',  # タスクの場所を指定
        'schedule': 60.0,  # 60秒ごとに実行
    },
}

app.autodiscover_tasks()
print('celery_config.py終了')