from testApp.celery_config import shared_task
from django.utils import timezone
from .models import Schedule

@shared_task
def delete_temporary_schedules():
    # 現在時刻から15分前の時間を取得
    threshold = timezone.now() - timezone.timedelta(minutes=15)

    # 仮予約フラグがTrueで、かつ15分以上経過している予約を取得
    schedules = Schedule.objects.filter(is_temporary=True, created_at__lte=threshold)

    # 取得した予約を削除
    schedules.delete()
