# challenge/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import GameBox
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameBox
import json


def challenge_view(request):
    context = {}  
    return render(request, 'challenge/challenge.html', context)

@csrf_exempt  # CSRF 토큰을 비활성화합니다. 실제 환경에서는 적절한 CSRF 보호를 사용해야 합니다.
@require_POST  # POST 요청만 허용합니다.
def update_gamebox_status(request):
    try:
        # 요청의 JSON 본문을 파싱합니다.
        data = json.loads(request.body)
        team_id = data.get('team_id')
        challenge_id = data.get('challenge_id')
        is_down = data.get('is_down')
        is_attacked = data.get('is_attacked')

        # 해당하는 GameBox 객체를 찾고 상태를 업데이트합니다.
        gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
        gamebox.is_down = is_down
        gamebox.is_attacked = is_attacked
        gamebox.save()

        # 성공 응답을 반환합니다.
        return JsonResponse({'status': 'success', 'message': 'GameBox status updated successfully.'})
    except GameBox.DoesNotExist:
        # GameBox 객체를 찾을 수 없는 경우
        return JsonResponse({'status': 'error', 'message': 'GameBox not found.'}, status=404)
    except Exception as e:
        # 기타 오류 처리
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_gamebox_data(request): # 멀티루틴-싱글루틴 처리필요
    challenge_id = request.GET.get('challenge_id')
    team_id = request.GET.get('team_id')
    if challenge_id and team_id:
        gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
        data = {
            'created_at': gamebox.created_at,
            'challenge_id': gamebox.challenge_id,
            'challenge_name': gamebox.challenge_name,
            'team_id': gamebox.team_id,
            'ip': gamebox.ip,
            'port': gamebox.port,
            'ssh_port': gamebox.ssh_port,
            'ssh_user': gamebox.ssh_user,
            'ssh_password': gamebox.ssh_password,
            'description': gamebox.description,
            'score': gamebox.score,
            'visible': gamebox.visible,
            'is_down': gamebox.is_down,
            'is_attacked': gamebox.is_attacked,
        }
    elif team_id:
        gameboxes = GameBox.objects.filter(team_id=team_id)
        data = [{
            'created_at': gamebox.created_at,
            'challenge_id': gamebox.challenge_id,
            'challenge_name': gamebox.challenge_name,
            'team_id': gamebox.team_id,
            'ip': gamebox.ip,
            'port': gamebox.port,
            'ssh_port': gamebox.ssh_port,
            'ssh_user': gamebox.ssh_user,
            'ssh_password': gamebox.ssh_password,
            'description': gamebox.description,
            'score': gamebox.score,
            'visible': gamebox.visible,
            'is_down': gamebox.is_down,
            'is_attacked': gamebox.is_attacked,
        } for gamebox in gameboxes]
    else:
        data = []
    return JsonResponse(data, safe=False)