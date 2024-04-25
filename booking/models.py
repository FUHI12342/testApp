from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db import models
from django.utils.crypto import get_random_string

class Timer(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)

class Store(models.Model):
    """店舗"""
    name = models.CharField('店名', max_length=255)

    def __str__(self):
        return self.name
        
class Staff(models.Model):
    """占い師スタッフ"""
    name = models.CharField('表示名', max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='ログインユーザー', on_delete=models.CASCADE
    )
    store = models.ForeignKey(Store, verbose_name='店舗', on_delete=models.CASCADE)
    line_id = models.CharField('LINE ID', max_length=50, null=True, blank=True)  # ラインID
    thumbnail = models.ImageField('サムネイル画像', upload_to='thumbnails/', null=True, blank=True)  # サムネイル画像
    introduction = models.TextField('自己紹介文', null=True, blank=True)  # 自己紹介文
    price = models.IntegerField('価格', default=0)  # 価格情報、デフォルト値を0に設定

    def __str__(self):
        return f'{self.store.name} - {self.name}'
    
class Customer(models.Model):
    line_user_id = models.CharField('LINEユーザーID', max_length=255)
    name = models.CharField('名前', max_length=255, null=True, blank=True)
    # 必要に応じて他のフィールドを追加

    def __str__(self):
        return self.name
    
from django.core.exceptions import ValidationError

def create_customer(line_user_id, name):  # その他のパラメーター
    if Customer.objects.filter(line_user_id=line_user_id).exists():
        raise ValidationError(f"Customer with line_user_id {line_user_id} already exists.")
    # その他のパラメーターとともにCustomerオブジェクトを作成
    customer = Customer(line_user_id=line_user_id, name=name)
    customer.save()

from django.conf import settings
import uuid

class Schedule(models.Model):
    """予約スケジュール."""
    reservation_number = models.CharField('予約番号', max_length=255, default=uuid.uuid4, editable=False)
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    staff = models.ForeignKey('Staff', verbose_name='占いスタッフ', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, verbose_name='顧客', on_delete=models.CASCADE, null=True, blank=True)
    is_temporary = models.BooleanField('仮予約フラグ', default=True)
    price = models.IntegerField('価格', default=0)  # 価格情報、デフォルト値を0に設定
    temporary_booked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.reservation_number} {start} ~ {end} {self.staff}'
