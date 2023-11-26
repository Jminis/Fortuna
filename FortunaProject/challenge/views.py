# challenge/views.py
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameBox


def challenge_view(request):
    context = {}
    return render(request, 'challenge/challenge.html', context)


def get_gamebox_data(request): # 멀티루틴-싱글루틴 처리필요
    challenge_id = request.GET.get('challenge_id')
    team_id = request.GET.get('team_id')
    print(challenge_id)
    print(team_id)
    if challenge_id and team_id:
        print(1)
        gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
        data = {
            'created_at': gamebox.created_at,
            'challenge_id': gamebox.challenge_id,
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
        print(2)
        gameboxes = GameBox.objects.filter(team_id=team_id)
        data = [{
            'created_at': gamebox.created_at,
            'challenge_id': gamebox.challenge_id,
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
        print(3)
        data = []
    return JsonResponse(data, safe=False)