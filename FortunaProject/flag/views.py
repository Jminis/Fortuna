from django.shortcuts import render
import hashlib
import secrets
from challenge.models import GameBox
from authentication.models import AuthInfo
from account.models import Team
from log.models import ActionTry
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse

def flag_view(request):
    auth_info = AuthInfo.objects.all()  # 모든 AuthInfo 인스턴스를 가져옵니다.
    round = get_round_info()  # 현재 라운드 정보를 가져옵니다.
#########################라운드 일괄 1    
    round = 1  # 현재 라운드 임시 설정
    round_info = AuthInfo.objects.filter(round=round)  # 현재 라운드의 AuthInfo 인스턴스를 가져옵니다.
    action_tries = ActionTry.objects.filter(round=round)

    teams = Team.objects.all()  # 모든 Team 인스턴스를 가져옵니다.

        # 각 AuthInfo 객체에 해당하는 GameBox ID를 저장할 리스트를 생성합니다.
    round_info_with_gamebox = []
    for info in round_info:
        try:
            # 해당하는 GameBox 인스턴스를 가져옵니다.
            gamebox = GameBox.objects.get(challenge_id=info.challenge_id, team_id=info.team_id)
            # AuthInfo 객체에 gamebox 인스턴스를 직접 추가합니다.
            info.gamebox = gamebox
        except GameBox.DoesNotExist:
            # GameBox 인스턴스가 존재하지 않는 경우
            info.gamebox = None
        
        # 수정된 AuthInfo 객체를 리스트에 추가합니다.
        round_info_with_gamebox.append(info)

    # 갱신된 round_info 리스트와 나머지 컨텍스트를 템플릿에 전달합니다.
    return render(request, 'flag/flag.html', {
        'auth_info': auth_info,
        'round_info': round_info_with_gamebox,
        'round': round,
        'action_tries': action_tries,
        'teams': teams,
    })

def generate_flag_for_gamebox(team_id, challenge_id):
    flags_created = []

    for round in range(1, 4):  # 모든 라운드에 대해 플래그 생성
        try:
            gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
            salt = secrets.token_hex(8)
            raw_flag = f"{round}{gamebox.challenge_id}{salt}"
            hashed_flag = hashlib.sha256(raw_flag.encode()).hexdigest()
            final_flag = f"SF{{{hashed_flag}}}"

            # AuthInfo 인스턴스에 플래그 저장 또는 갱신
            obj, created = AuthInfo.objects.get_or_create(
                challenge_name=gamebox.challenge_name,
                team_id=gamebox.team_id,
                challenge_id=gamebox.challenge_id,
                round=round,
                defaults={'flag': final_flag}
            )
            if not created:
                obj.flag = final_flag
                obj.save()

            flags_created.append(final_flag)

        except GameBox.DoesNotExist:
            continue  # 해당 team_id와 challenge_id를 가진 GameBox가 없는 경우

    return flags_created

def create_one_flag(request, team_id, challenge_id):
    if request.method == 'POST':
        generate_flag_for_gamebox(team_id, challenge_id)
        return HttpResponseRedirect(reverse('flag'))  # 플래그 관리 페이지로 리다이렉트
    else:
        return HttpResponse("Method not allowed.", status=405)

def create_flag():
    gameboxes = GameBox.objects.all()
    all_flags_created = []

    for gamebox in gameboxes:
        flags_created = generate_flag_for_gamebox(gamebox.team_id, gamebox.challenge_id)
        all_flags_created.extend(flags_created)

    return all_flags_created


def create_flag_view(request):
    create_flag()  # 플래그 생성
    return HttpResponseRedirect(reverse('flag'))  # 플래그 관리 페이지로 리다이렉트

def export_authinfo_to_txt(request):
    # AuthInfo의 모든 인스턴스를 가져옵니다.
    authinfo_objects = AuthInfo.objects.all()

    # 각 인스턴스의 내용을 문자열로 변환합니다.
    lines = []
    for obj in authinfo_objects:
        line = f"Challenge Name: {obj.challenge_name}, Team ID: {obj.team_id}, Challenge ID: {obj.challenge_id}, Round: {obj.round}, Flag: {obj.flag}"
        lines.append(line)

    # 응답 객체를 생성하여 파일로 내보냅니다.
    response = HttpResponse("\n".join(lines), content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="flag.txt"'

    return response

def get_action_tries_for_team(request, team_name):
    action_tries = ActionTry.objects.filter(attacker_name=team_name, round=1)
    data = serializers.serialize('json', action_tries)
    return JsonResponse(data, safe=False)

def get_round_info():
    # 라운드 정보를 반환하는 함수
    # 이 부분은 라운드 정보를 어떻게 관리하는지에 따라 달라집니다.
    pass

