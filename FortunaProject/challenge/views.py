# challenge/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import GameBox, Challenge
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import GameBox
from .forms import GameBoxForm, ChallengeForm
import json
from account.models import Team

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
            'description': gamebox.description,
            'score': gamebox.score,
            'visible': gamebox.visible,
            'is_down': gamebox.is_down,
            'is_attacked': gamebox.is_attacked,
        } for gamebox in gameboxes]
    else:
        data = []
    return JsonResponse(data, safe=False)

def create_gamebox(request):
    if request.method == "POST":
        challenge_id = request.POST.get('challenge_id')
        challenge_name = request.POST.get('challenge_name')
        team_id = request.POST.get('team_id')
        description = request.POST.get('description')
        visible = True
        score = 0
        is_down = False
        is_attacked = False
        
        gamebox = GameBox(
            challenge_id=challenge_id,
            challenge_name=challenge_name,
            team_id=team_id,
            description = description,
            visible = visible,
            score = score,
            is_down = is_down,
            is_attacked = is_attacked,
        )
        gamebox.save()
        return redirect('challenge/manage_challenge.html')

    return render(request, 'challenge/manage_challenge.html')

## Manage Page View
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
    forms = {gamebox: ChallengeForm(instance=gamebox) for gamebox in gameboxes}
    challenges = Challenge.objects.all()

    # 수정 요청 처리
    if 'edit_gamebox' in request.POST:
        gamebox_id = request.POST.get('gamebox_id')
        gamebox = get_object_or_404(GameBox, pk=gamebox_id)
        edit_form = ChallengeForm(request.POST, instance=gamebox)
        if edit_form.is_valid():
            edit_form.save()
    context = {'gameboxes': gameboxes, 'form': form, 'forms': forms, 'teams': teams, 'challenges': challenges}
    return render(request, 'challenge/manage_challenge.html', context)


def update_gamebox_view(request, id):
    gamebox = get_object_or_404(GameBox, pk=id)
    form = ChallengeForm(request.POST or None, instance=gamebox)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('manage_challenge')

    return render(request, 'edit_gamebox.html', {'form': form})

def delete_gamebox_view(request, id):
    gamebox = get_object_or_404(GameBox, pk=id)
    if request.method == "POST":
        gamebox.delete()
    return redirect('manage_challenge')

def upsert_challenge_view(request):
    Challenge.objects.all().delete()
    print(1)

    team_count = Team.objects.count()
    challenge_count = GameBox.objects.count()
    print(team_count)
    print(challenge_count)
    for i in range(1, team_count + 1):
        for j in range(1, challenge_count + 1):
            ip = f'192.168.1.{j}00{i}'
            port = j*1000 + i
            ssh_port = j*100+i
            ssh_username = f'user{i}'
            ssh_password = f'1234{i}'
            Challenge.objects.create(
                ip = ip,
                port = port,
                ssh_port = ssh_port,
                ssh_user = ssh_username,
                ssh_password = ssh_password
            )

    return redirect('manage_challenge')