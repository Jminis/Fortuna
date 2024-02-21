from django.http import JsonResponse
from django.shortcuts import render
from log.models import ActionLog
from config.models import Config

def log_view(request):
    # DB에서 최근 50개의 로그 데이터 가져오기
    actions = ActionLog.objects.all().order_by('-created_at')[:50]
    # 가장 최근에 생성된 Config 인스턴스 가져오기
    config = Config.objects.latest('created_at')

    print(actions)
    print(config)

    # actions와 config를 템플릿에 전달
    return render(request, 'log/log_.html', {'actions': actions, 'config': config})
