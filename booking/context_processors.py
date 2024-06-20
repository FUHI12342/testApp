from .models import Company, Notice, Media

def global_context(request):
    company = Company.objects.first()  # 最初のCompanyインスタンスを取得
    notices = Notice.objects.all()  # 全てのNoticeインスタンスを取得
    medias = Media.objects.all()  # 全てのMediaインスタンスを取得
    return {'company': company, 'notices': notices, 'medias': medias}  # 'media'を'medias'に変更