from django.http import JsonResponse
from django.shortcuts import render
from log.models import ActionLog
import json


def log_view(request):
    # DB에서 로그 데이터 가져오기
    actions = ActionLog.objects.all().order_by('-created_at')[:50]  #최근 50개의 로그
    print(request.user)
    return render(request, 'log/log_.html', {'actions': actions})
