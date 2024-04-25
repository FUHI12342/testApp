from django.contrib import admin
from .models import Staff, Store, Schedule


""" Django 管理サイト名変更 """
admin.site.site_header = '占いサロンチャンス管理ページ'

""" サイト管理名変更 """
admin.site.index_title = '店舗/在籍占い師/スケジュールリスト'

admin.site.register(Staff)
admin.site.register(Store)
admin.site.register(Schedule)
