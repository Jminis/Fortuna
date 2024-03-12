import json, os
from django.conf import settings
from django.shortcuts import render
from account.models import Team
from log.models import ActionLog
from config.models import Config
from django.utils import timezone

config_path = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

def index_view(request):
    # load_config_data 함수(또는 설정 데이터를 불러오는 다른 메커니즘)를 통해 설정 데이터를 불러옵니다.
    context = {
        'config': config_data['index'],
    }
    
    return render(request, 'index.html', context)

def play_view(request):
    actions = ActionLog.objects.all().order_by('created_at')[:50]
    try:
        config = Config.objects.latest('created_at')
        #라운드 계산
        now = timezone.localtime()
        elapsed_time = now - timezone.localtime(config.starttime)
        total_minutes = int(elapsed_time.total_seconds() // 60)
        current_round = total_minutes // config.round_time
    except Config.DoesNotExist:
        config = 0
        current_round = 0   
    
    context = {'actions': actions, 'config': config, 'round':current_round}
    return render(request, 'play.html', context)