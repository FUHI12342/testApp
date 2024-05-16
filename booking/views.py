from __future__ import absolute_import, unicode_literals
import datetime
import json
import jwt
import requests
import secrets
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View
from django.views.decorators.http import require_POST
from booking.models import Store, Staff, Schedule, Customer, Timer
import sys
print('環境変数1' + str(sys.path))

User = get_user_model()
class Index(generic.TemplateView):
    template_name = 'booking/index.html'


class LineEnterView(View):
    def get(self, request):
        # ランダムなstateを生成し、セッションに保存します。
        state = secrets.token_hex(10)
        request.session['state'] = state
        
        print('セッション' + str(request.session.items())) 
        
        context = {
            'channel_id': LINE_CHANNEL_ID,
            'redirect_url': REDIRECT_URL,
            'random_state': state,
        }
        return render(request, 'booking/line_login.html', context)

    def post(self, request):
        # POSTリクエストを処理します。
        # ここでは、例として同じcontextを使用しますが、
        # 実際にはPOSTリクエストのデータに基づいてcontextを更新することが一般的です。
        state = secrets.token_hex(10)
        request.session['state'] = state
        context = {
            'channel_id': LINE_CHANNEL_ID,
            'redirect_url': REDIRECT_URL,
            'random_state': state,
        }
        return render(request, 'booking/line_login.html', context)
    
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

def LINETimerView(request, user_id):
    # タイマーの開始時刻をデータベースに保存します
    timer, created = Timer.objects.get_or_create(user_id=user_id, defaults={'start_time': timezone.now()})

    if not created:
        # 既存のタイマーを更新する場合の処理
        timer.start_time = timezone.now()
        timer.save()

    # タイマーの終了時間を設定します（ここでは開始時間から10分後とします）
    timer.end_time = timer.start_time + timedelta(minutes=60)
    timer.save()

    # 終了時間をcontextに追加します
    context = {'end_time': timer.end_time}

    # timer.htmlテンプレートをレンダリングします
    return render(request, 'booking/timer.html', context)

# 終了時間を保存する変数
# ここではサーバー起動時から1時間後を終了時間としています
end_time = timezone.now() + timedelta(hours=1)

def get_end_time(request):
    # 終了時間をISO 8601形式の文字列として返す
    return JsonResponse({'time': end_time.isoformat()})

def get_current_time(request):
    # 現在時間をISO 8601形式の文字列として返す
    return JsonResponse({'time': timezone.now().isoformat()})

def get_reservation_times(request, pk):
    # pkを使用して予約を取得
    schedule = get_object_or_404(Schedule, pk=pk)
    # 開始時間と終了時間をISO 8601形式の文字列として返す
    return JsonResponse({'startTime': schedule.start.isoformat(), 'endTime': schedule.end.isoformat()})



def get_reservation(request, pk):
    # pkを使用して予約を取得
    schedule = get_object_or_404(Schedule, pk=pk)
    # 開始時間と終了時間をISO 8601形式の文字列として返す
    return JsonResponse({
        'startTime': schedule.start.isoformat(),
        'endTime': schedule.end.isoformat()
    })


     
class CurrentTimeView(APIView):
    def get(self, request):
        import datetime
        current_time = datetime.datetime.now()
        return Response({"current_time": str(current_time)})
    
    
from django.http import HttpResponseBadRequest

LINE_CHANNEL_ID = settings.LINE_CHANNEL_ID  # 自身のLINEチャンネルIDを入力
LINE_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET
REDIRECT_URL = settings.LINE_REDIRECT_URL

class LineCallbackView(View):
        def get(self, request):
            context = {}
            code = request.GET.get('code')
            state = request.GET.get('state')

            # stateがセッションに保存されたものと一致することを確認します。
            if state != request.session.get('state'):
                return HttpResponseBadRequest()
            
            # 認可コードを取得する
            uri_access_token = "https://api.line.me/oauth2/v2.1/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            if code is not None:
                data_params = {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URL,
                    "client_id": LINE_CHANNEL_ID,
                    "client_secret": LINE_CHANNEL_SECRET
                }
                # トークンを取得するためにリクエストを送る
                response_post = requests.post(uri_access_token, headers=headers, data=data_params)

                if response_post.status_code == 200:
                    # 今回は"id_token"のみを使用する
                    line_id_token = json.loads(response_post.text)["id_token"]
                    # ペイロード部分をデコードすることで、ユーザ情報を取得する
                    user_profile = jwt.decode(line_id_token,
                                    LINE_CHANNEL_SECRET,
                                    audience=LINE_CHANNEL_ID,
                                    issuer='https://access.line.me',
                                    algorithms=['HS256'],
                                    options={'verify_iat': False})
                    # LINE登録のユーザー情報を表示する場合は、contextに追加しておく
                    context["user_profile"]=user_profile

                    # LINEユーザーIDを取得
                    line_user_id = user_profile['sub']

                    try:
                        customer = Customer.objects.get(line_user_id=line_user_id)
                    except Customer.DoesNotExist:
                        print("Customerが存在しません。")
                        customer = None

                    if customer is not None:
                        # LINEユーザーIDを設定
                        customer.line_user_id = line_user_id

                        # インスタンスを保存
                        customer.save()

                    from linebot import LineBotApi
                    from linebot.models import TextSendMessage
                    from linebot.exceptions import LineBotApiError
                
                    # LINE Messaging APIの初期化
                    line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)

                    #ユーザーIDとメッセージ
                    #ユーザーIDはログイン後に取得
                    user_id = user_profile['sub']  #'sub'はLINEのユーザーIDを表す
                   
                    try:
                        # ユーザープロファイルの取得
                        profile = line_bot_api.get_profile(user_id)
                        # ユーザーIDとメッセージ
                        user_id = profile.user_id
                        
                        from datetime import datetime, timedelta
                        # 現在の日時を取得
                        now = datetime.now()

                        # 現在の日時から1日後の日時を取得
                        expired_on = now + timedelta(days=1)

                        # expired_onをISO 8601形式の文字列に変換
                        expired_on_str = expired_on.strftime('%Y-%m-%d')

                        # 仮予約情報をセッションから取得
                        temporary_booking = request.session.get('temporary_booking')

                        if temporary_booking is not None:
                            # 価格情報を取得
                            price = temporary_booking['price']
                            schedule_reservation_number = temporary_booking['reservation_number']
                            
                        else:
                            print("仮予約情報がセッションに存在しません。")
                            price = None  # または適切なデフォルト値を設定

                        # 決済サービスのAPIを使用して決済URLを生成
                        payment_api_url = settings.PAYMENT_API_URL
                        headers = {
                            'Authorization': 'Bearer ' + settings.PAYMENT_API_KEY,
                            'Content-Type': 'application/json'  
                        }

                        # Webhook URLを動的に設定
                        webhook_url = settings.WEBHOOK_URL_BASE + str(schedule_reservation_number)

                        data = {
                            "amount": price,  # 仮予約情報から取得した価格情報を設定
                            "currency": "jpy",
                            "locale": "ja_JP",
                            "cancelUrl": settings.CANCEL_URL,
                            "webhookUrl": webhook_url,  # ここで設定
                            "method": "creditcard",
                            "subject": "ご予約料金",
                            "description": "ウェブサイトからの支払い",
                            "remarks": "仮予約から10分を過ぎますと自動的にキャンセルとなります。あらかじめご了承ください。",
                            "metadata": {
                                "orderId":schedule_reservation_number
                            },
                            "expiredOn": expired_on_str
                        }
                        # 以下のコードは変更なし...
                        payment_url = None  # 初期化

                        response = requests.post(payment_api_url, headers=headers, data=json.dumps(data))  # json.dumpsを使用
                        if response.status_code == 201:
                            try:
                                payment_url = response.json()['links']['paymentUrl']
                            except ValueError:
                                print("Error decoding JSON")
                        else:
                            print("HTTP request failed with status code ", response.status_code)
                            print("Response body: ", response.content)
                        #LINE Messaging APIを使用してメッセージを送信
                        message = None  # 初期化

                        if payment_url is not None:
                            message = TextSendMessage(text='こちらのURLから決済を行ってください。決済後に予約が確定します。: ' + payment_url)
                            line_bot_api.push_message(user_id, message)
                            print("Message sent successfully")
                        else:
                            print("Payment URL is not available") 
                        
                    except LineBotApiError as e:
                        print("Failed to send message: ", e)
                        if e.status_code == 404:
                            print('ユーザーがボットを友達登録していません')

                    # ユーザープロファイル情報をセッションに保存
                    request.session['profile'] = user_profile
                    print('セッション情報' + str(request.session.items()))
                                    
                    return render(request, 'booking/line_success.html', {'profile': user_profile})      
                else:
                    print('トークンの取得に失敗しました')
                return HttpResponse('トークンの取得に失敗しました')
            
from django.http import JsonResponse
from django.views import View
from linebot import LineBotApi
from linebot.models import TextSendMessage
from django.urls import reverse
from urllib.parse import quote
from linebot.exceptions import LineBotApiError
import json


class PayingSuccessView(View):
    def post(self, request, reservation_number):
        # 決済サービスからのレスポンスを解析
        payment_response = json.loads(request.body)
        return process_payment(payment_response, request, reservation_number)
    
class LineSuccessView(View):
    def get(self, request):
        # セッションからプロフィールを取得します。
        profile = request.session.get('profile')

        return render(request, 'booking/line_success.html', {'profile': profile})
    
   
class OnlyStaffMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        return staff.user == self.request.user or self.request.user.is_superuser


class OnlyScheduleMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return schedule.staff.user == self.request.user or self.request.user.is_superuser


class OnlyUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.kwargs['pk'] == self.request.user.pk or self.request.user.is_superuser


class StoreList(generic.ListView):
    model = Store
    ordering = 'name'


class StaffList(generic.ListView):
    model = Staff
    ordering = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.store
        return context

    def get_queryset(self):
        store = self.store = get_object_or_404(Store, pk=self.kwargs['pk'])
        queryset = super().get_queryset().filter(store=store)
        return queryset


class StaffCalendar(generic.TemplateView):
    template_name = 'booking/calendar.html'

    def get_context_data(self, **kwargs):
        print(datetime.date)  # ここを追加
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(9, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=17, minute=0, second=0))
        
        for schedule in Schedule.objects.filter(staff=staff).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                # 予約が仮予約の場合は値を'Temp'に、そうでない場合は'Booked'に設定
                calendar[booking_hour][booking_date] = 'Temp' if schedule.is_temporary else 'Booked'

        context['staff'] = staff
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context
    
from django import forms

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = []  # Scheduleモデルのフィールドを指定

import pytz

class PreBooking(generic.CreateView):
    print('プリブッキング')
    model = Schedule
    form_class = ScheduleForm
    template_name = 'booking/booking.html'
    
    def get_context_data(self, **kwargs):
        print('ゲットコンテキストデータ')
        context = super().get_context_data(**kwargs)
        context['staff'] = get_object_or_404(Staff, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)  # POSTデータを出力
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        print('form_invalid:', form.errors)  # フォームのエラーを出力
        return super().form_invalid(form)
    
    def form_valid(self, form):
        print('フォームバリッド')
        print('form.is_valid()の結果:', form.is_valid())        
        print('form.errorsの結果:', form.errors)
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        # StaffからPriceを取得
        price = staff.price
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        day = int(self.kwargs.get('day'))
        hour = int(self.kwargs.get('hour'))
        tz = pytz.timezone(settings.TIME_ZONE)
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        
        # 既存のスケジュールがあるかどうかを確認
        if Schedule.objects.filter(staff=staff, start=start).exists():
            print("既に同じスタッフと開始時間でスケジュールが存在します。")
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule = form.save(commit=False)
            schedule.staff = staff
            schedule.start = start
            schedule.end = end
            schedule.is_temporary = True  # 仮予約フラグを設定
            schedule.price = price  # 価格を設定
            schedule.temporary_booked_at = datetime.datetime.now(tz)  # 仮予約日時を設定

            customer = Customer()  # 新しいCustomerインスタンスを作成
            # 必要な情報を設定（ここでは例としてnameフィールドを設定）
            customer.name = '取得した名前'
            customer.save()  # インスタンスを保存
            
          
            if customer.pk is not None:
                print("Customerインスタンスの作成と保存が成功しました。")
                schedule.customer = customer  # 作成したCustomerインスタンスをScheduleに紐づける
            else:
                print("Customerインスタンスの作成と保存に失敗しました。")

            schedule.save()
            print('仮予約完了')
            
            
           # 仮予約情報をセッションに保存
            self.request.session['temporary_booking'] = {
                'reservation_number': str(schedule.reservation_number),
                'customer_id': customer.id,
                'start': start.isoformat(),
                'end': end.isoformat(),
                'price': price,
            }


        return redirect('booking:line_enter')
    
from linebot import LineBotApi
from linebot.models import TextSendMessage

class CancelReservationView(View):
    def post(self, request, schedule_id):
        # 予約情報を取得
        schedule = Schedule.objects.get(id=schedule_id)

        # 予約をキャンセル
        schedule.is_cancelled = True
        schedule.save()

        # LINE Messaging APIの初期化
        line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)

        # 予約者のLINEアカウントIDを取得
        customer_line_account_id = schedule.customer.line_id

        # キャンセル情報をメッセージとして送信
        message_text = 'あなたの予約がキャンセルされました。予約日時: {}'.format(schedule.start)
        message = TextSendMessage(text=message_text)
        line_bot_api.push_message(customer_line_account_id, message)

        return render(request, 'booking/cancel_success.html')

class MyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'booking/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_list'] = Staff.objects.filter(user=self.request.user).order_by('name')
        context['schedule_list'] = Schedule.objects.filter(staff__user=self.request.user, start__gte=timezone.now()).order_by('user')
        return context


class MyPageWithPk(OnlyUserMixin, generic.TemplateView):
    template_name = 'booking/my_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context['staff_list'] = Staff.objects.filter(user__pk=self.kwargs['pk']).order_by('name')
        context['schedule_list'] = Schedule.objects.filter(staff__user__pk=self.kwargs['pk'], start__gte=timezone.now()).order_by('user')
        return context


class MyPageCalendar(OnlyStaffMixin, StaffCalendar):
    template_name = 'booking/my_page_calendar.html'


class MyPageDayDetail(OnlyStaffMixin, generic.TemplateView):
    template_name = 'booking/my_page_day_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        staff = get_object_or_404(Staff, pk=pk)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.date(year=year, month=month, day=day)

        # 9時から17時まで1時間刻みのカレンダーを作る
        calendar = {}
        for hour in range(9, 18):
            calendar[hour] = []

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(date, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(date, datetime.time(hour=17, minute=0, second=0))
        for schedule in Schedule.objects.filter(staff=staff).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar:
                calendar[booking_hour].append(schedule)

        context['calendar'] = calendar
        context['staff'] = staff
        return context


class MyPageSchedule(OnlyScheduleMixin, generic.UpdateView):
    model = Schedule
    fields = ('start', 'end', 'user')
    success_url = reverse_lazy('booking:my_page')


class MyPageScheduleDelete(OnlyScheduleMixin, generic.DeleteView):
    model = Schedule
    success_url = reverse_lazy('booking:my_page')

print('環境変数2' + str(sys.path))
from django.shortcuts import render
from .forms import YourForm

def your_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            # フォームのデータを処理します
            pass
    else:
        form = YourForm()

    return render(request, 'your_template.html', {'form': form})

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
import datetime

@require_POST
def my_page_holiday_add(request, pk, year, month, day, hour):
    staff = get_object_or_404(Staff, pk=pk)
    if staff.user == request.user or request.user.is_superuser:
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        Schedule.objects.create(staff=staff, start=start, end=end, user=request.user)
        return redirect('booking:my_page_day_detail', pk=pk, year=year, month=month, day=day)

    raise PermissionDenied

@require_POST
def my_page_day_add(request, pk, year, month, day):
    staff = get_object_or_404(Staff, pk=pk)
    hour=9
    if staff.user == request.user or request.user.is_superuser:
            for num in range(9):
                start = datetime.datetime(year=year, month=month, day=day, hour=hour+num)
                end = datetime.datetime(year=year, month=month, day=day, hour=hour+num+1)
                Schedule.objects.create(staff=staff, start=start, end=end, user=request.user)
            return redirect('booking:my_page_day_detail', pk=pk, year=year, month=month, day=day)
    raise PermissionDenied

@require_POST
def my_page_day_delete(request, pk, year, month, day):
    staff = get_object_or_404(Staff, pk=pk)
    if staff.user == request.user or request.user.is_superuser:
        start = datetime.datetime(year=year, month=month, day=day, hour=9)
        end = datetime.datetime(year=year, month=month, day=day, hour=17)
        Schedule.objects.filter(staff=staff, start__gte=start, end__lte=end).delete()
        return redirect('booking:my_page_day_detail', pk=pk, year=year, month=month, day=day)

    raise PermissionDenied

print('ビューのタスク.py')
@shared_task
def delete_temporary_schedules():
    print('delete_temporary_schedules')
    # 関数の本体
    now = timezone.now()
    print(str(now) + "現在時刻")
    
    Schedule.objects.filter(temporary_booked_at__lt=now - timezone.timedelta(minutes=10), is_temporary=True).delete()
    print('delete_temporary_schedules終了')
    
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StaffForm  # Django管理画面でのフォームに対応するフォームをインポートします

def upload_file(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        print('フォームの中身' + str(form))
        if form.is_valid():
            form.save()
            print('フォームのセーブ')
            return HttpResponseRedirect('/success/url/')  # 成功時のリダイレクト先URLを指定します
        else:
            print('フォームのエラー'+ form.errors)
    else:
        form = StaffForm()
        print('フォームの中身２' + str(form))
    return render(request, 'upload.html', {'form': form})

import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt

def process_payment(payment_response, request):
    print('payment_response' + str(payment_response))
    
    # 決済が成功したかどうかを確認
    if payment_response.get('type') == 'payment.succeeded':
        # 注文IDを取得
        order_id = payment_response.get('orderId')
        schedule = Schedule.objects.get(order_id=order_id)
        print('スケジュール' + str(schedule))
        
        # 仮予約フラグをFalseに設定
        schedule.is_temporary = False

        # 予約情報を保存
        schedule.save()
        print('本予約情報として保存')
        
         # LINE Messaging APIの初期化
        line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)

        # スタッフのLINEアカウントIDを取得
        staff_line_account_id = schedule.staff.line_id
        import pytz

        # ローカルタイムゾーンを取得
        local_tz = pytz.timezone('Asia/Tokyo')

        # schedule.startをローカルタイムゾーンに変換
        local_time = schedule.start.astimezone(local_tz)
        
        print('スタッフのLINEアカウントID:' + str(staff_line_account_id))
        print(schedule.start)
        try:
            # 予約完了情報をメッセージとして送信
            message_text = '予約が完了しました。予約者: {}, 日時: {}'.format(schedule.customer.name, local_time)
            message = TextSendMessage(text=message_text)
            line_bot_api.push_message(staff_line_account_id, message)  # スタッフに通知
            print('スタッフに通知')
            print(message_text)
            
        except LineBotApiError as e:
            # エラーハンドリング
            print(e)
            
    # セッションからプロフィールを取得します。
    profile = request.session.get('profile')
    user_id = profile['sub']  # 'sub'はLINEのユーザーIDを表す

    # LINE Messaging APIの初期化
    line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)
    
    # タイマーURLを生成
    timer_url = reverse('booking:LINETimerView', args=[user_id])
    encoded_timer_url = quote(timer_url)

    # 決済完了の通知とタイマーURLをメッセージとして送信（予約キャンセルもこの先）
    message_text = '決済が完了しました。こちらのURLから予約情報・タイマーを確認できます: ' + '<' + 'https://timebaibai.com/' + encoded_timer_url + '>'
    message = TextSendMessage(text=message_text)
    line_bot_api.push_message(user_id, message)
    print('ユーザーに通知')
    print(message_text)
    
    # レスポンスを直接作成して返す
    return JsonResponse({'status': 'success'})

@csrf_exempt
def coiney_webhook(request, reservation_number):
    if request.method == 'POST':
        # Coineyからの署名を取得
        signature = request.META.get('HTTP_X_COINEY_SIGNATURE')

        # リクエストボディとシークレットキーを使用して署名を計算
        expected_signature = hmac.new(
            bytes(settings.PAYMENT_API_KEY, 'utf-8'),
            msg=request.body,
            digestmod=hashlib.sha256
        ).hexdigest()

        # 受信した署名と計算した署名を比較
        if not hmac.compare_digest(signature, expected_signature):
            return JsonResponse({'error': 'invalid signature'}, status=400)

        # 署名が一致した場合、PayingSuccessViewのpostメソッドを呼び出す
        # ここで予約番号を渡す
        return PayingSuccessView.post(request, reservation_number)
    else:
        return JsonResponse({'error': 'invalid request'}, status=400)
