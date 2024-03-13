from django.shortcuts import render
from .models import Config

# Create your views here.
def config_view(request):
    # config = Config.objects.first()  # Config 모델의 첫 번째 레코드를 가져옴
    config = Config.objects.latest('created_at')
    context = {'config': config}
    return render(request, 'manage/manage_config.html', context)