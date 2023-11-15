# challenge/views.py
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import GameBox

def challenge_view(request):
    context = { }
    return render(request, 'challenge/challenge.html', context)

def get_gamebox_data(request):
    challenge_id = request.GET.get('challenge_id')
    gamebox = GameBox.objects.get(id=challenge_id)
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
    return JsonResponse(data)

def test_data(request):
    # GameBox 인스턴스 생성
    test_game_box = GameBox(
        created_at=datetime.now(),  # 현재 시간
        challenge_id=123,  # 챌린지 ID
        team_id="teamA",  # 팀 ID
        ip='192.168.0.1',  # IP 주소
        port= 8080,  # 포트 번호
        ssh_port= 22,  # SSH 포트
        ssh_user='user',  # SSH 사용자명
        ssh_password='password',  # SSH 비밀번호
        description='이 챌린지는 끝내주게 재미있는 문제로 구성되어 있으며 들어가자마자 절망의 구렁텅이에 빠지게 됩니다',  # 설명
        visible=True,  # 가시성
        score=9.5,  # 점수
        is_down=False,  # 다운 여부
        is_attacked=False  # 공격받았는지 여부
    )
    # 데이터베이스에 저장 (선택적)
    test_game_box.save()