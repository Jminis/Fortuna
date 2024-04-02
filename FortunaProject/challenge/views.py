# challenge/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import GameBox, Challenge
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .forms import ChallengeForm
import json
from account.models import Team
from config.models import Config
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

## User Page View
def challenge_view(request):
    context = {}
    return render(request, 'challenge/challenge.html', context)

## Manage Page View
@admin_required
def manage_gamebox_view(request):
    # 새 GameBox 객체를 추가하기 위한 폼
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_challenge')  # 또는 다른 적절한 리다이렉션
    else:
        form = ChallengeForm()

    gameboxes = GameBox.objects.all()
    teams = Team.objects.all()
    challenges = Challenge.objects.all()
    context = {'gameboxes': gameboxes, 'form': form, 'teams': teams, 'challenges': challenges}
    return render(request, 'challenge/manage_challenge.html', context)

@csrf_exempt  # CSRF 토큰을 비활성화합니다. 실제 환경에서는 적절한 CSRF 보호를 사용해야 합니다.
@require_POST  # POST 요청만 허용합니다.
@admin_required
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

def get_gamebox_data(request):
    challenge_id = request.GET.get('challenge_id')
    team_id = request.GET.get('team_id')
    data = []  # 데이터 초기화

    if challenge_id and team_id:
        try:
            gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
            try:
                challenge = Challenge.objects.get(challenge_id=gamebox.challenge_id)
            except Challenge.DoesNotExist:
                challenge = None
            data = [{
                'created_at': gamebox.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # 날짜 포맷 수정
                'challenge_id': gamebox.challenge_id,
                'challenge_name': challenge.challenge_name if challenge else "챌린지 없음",
                'team_id': gamebox.team_id,
                'description': challenge.description if challenge else "설명 없음",
                'score': gamebox.score,
                'visible': gamebox.visible,
                'is_down': gamebox.is_down,
                'is_attacked': gamebox.is_attacked,
                'ip': gamebox.ip,
                'port': gamebox.port
            }]
        except GameBox.DoesNotExist:
            data = {'error': 'GameBox not found.'}

    elif team_id:
        gameboxes = GameBox.objects.filter(team_id=team_id)
        for gamebox in gameboxes:
            try:
                challenge = Challenge.objects.get(challenge_id=gamebox.challenge_id) # 챌린지 정보 받아옴
            except Challenge.DoesNotExist:
                challenge = None
            data.append({
                'created_at': gamebox.created_at,
                'challenge_id': gamebox.challenge_id,
                'challenge_name': challenge.challenge_name if challenge else "챌린지 없음",
                'team_id': gamebox.team_id,
                'description': challenge.description if challenge else "설명 없음",
                'score': gamebox.score,
                'visible': gamebox.visible,
                'is_down': gamebox.is_down,
                'is_attacked': gamebox.is_attacked,
            })

    return JsonResponse(data, safe=False if isinstance(data, list) else True)

def upsert_challenge_view(request):
    GameBox.objects.all().delete()
    config = Config.objects.all().first()
    challenges = Challenge.objects.all()
    team_count = Team.objects.count()

    for i in range(1, team_count + 1):
        for challenge in challenges:
            team_id = i
            challenge_id = challenge.challenge_id
            ip = challenge.ip
            port = challenge.challenge_id*1000 + i
            ssh_port = challenge.challenge_id*100+i
            ssh_username = f'user{i}'
            ssh_password = f'1234{i}'
            visible = True
            score = config.point_base
            is_down = False
            is_attacked = False
            GameBox.objects.create(
                team_id = team_id,
                challenge_id = challenge_id,
                ip = ip,
                port = port,
                ssh_port = ssh_port,
                ssh_user = ssh_username,
                ssh_password = ssh_password,
                visible = visible,
                score = score,
                is_down = is_down,
                is_attacked = is_attacked
            )

    return redirect('manage_challenge')
