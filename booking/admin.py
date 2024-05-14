from django.contrib import admin
from .models import Staff, Store, Schedule


""" Django 管理サイト名変更 """
admin.site.site_header = '占いサロンチャンス管理ページ'
admin.site.index_title = '店舗/在籍占い師/スケジュールリスト'


class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail')  # 'name'と'thumbnail'を表示する

admin.site.register(Staff, StaffAdmin)
admin.site.register(Store)
admin.site.register(Schedule)
