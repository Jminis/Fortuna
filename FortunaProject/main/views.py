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

def competition_time_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        try:
            latest_config = Config.objects.latest('created_at')
            if latest_config.starttime <= now <= latest_config.endtime:
                elapsed_time = now - timezone.localtime(latest_config.starttime)
                total_minutes = int(elapsed_time.total_seconds() // 60)
                current_round = total_minutes // latest_config.round_time
                kwargs['current_round'] = current_round  # current_round를 kwargs에 추가
                return view_func(request, *args, **kwargs)
            else:
                kwargs['current_round'] = -1  # 대회 진행 시간이 아닐 경우
                return view_func(request, *args, **kwargs)
        except Config.DoesNotExist:
            kwargs['current_round'] = -1  # Config가 존재하지 않을 경우
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@competition_time_required
def play_view(request, current_round):  # current_round를 인자로 받음
    actions = ActionLog.objects.all().order_by('created_at')[:50]
    context = {'actions': actions, 'round': current_round}
    return render(request, 'play.html', context)