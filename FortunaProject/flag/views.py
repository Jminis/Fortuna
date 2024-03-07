from django.shortcuts import render
import hashlib
import secrets
from challenge.models import GameBox
from authentication.models import AuthInfo
from account.models import Team
from config.models import Config
from log.models import ActionTry
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone

def get_round_info():
    # 현재 시간과 대회 시작 시간을 비교하여 현재 라운드 계산
    try:
        config = Config.objects.latest('created_at')
        
        now = timezone.localtime()
        elapsed_time = now - timezone.localtime(config.starttime)
        total_minutes = int(elapsed_time.total_seconds() // 60)
        current_round = total_minutes // config.round_time
        return current_round
    except Config.DoesNotExist:
        return 1  # Config가 없는 경우 기본값으로 1 반환

def flag_view(request):
    auth_info = AuthInfo.objects.all()  # 모든 AuthInfo 인스턴스를 가져옵니다.
    round = get_round_info()  # 현재 라운드 정보를 가져옵니다.
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

def calculate_rounds():
    try:
        config = Config.objects.latest('created_at')
        total_duration = timezone.localtime(config.endtime) - timezone.localtime(config.starttime)
        total_minutes = total_duration.total_seconds() // 60
        # 각 라운드의 지속 시간으로 전체 기간을 나누어 총 라운드 수를 계산
        total_rounds = int(total_minutes // config.round_time)
        return 0, total_rounds  # 첫 라운드와 마지막 라운드 번호 반환
    except Config.DoesNotExist:
        return 1, 1  # Config가 없는 경우 기본적으로 하나의 라운드만 있다고 가정

def generate_flag_for_gamebox(team_id, challenge_id):
    flags_created = []
    first_round, last_round = calculate_rounds()  # 첫 라운드와 마지막 라운드 계산

    for rounds in range(first_round, last_round+1):  # 모든 라운드에 대해 플래그 생성
        try:
            gamebox = GameBox.objects.get(team_id=team_id, challenge_id=challenge_id)
            salt = secrets.token_hex(8)
            raw_flag = f"{rounds}{gamebox.challenge_id}{salt}"
            hashed_flag = hashlib.sha256(raw_flag.encode()).hexdigest()
            final_flag = f"SF{{{hashed_flag}}}"

            # AuthInfo 인스턴스에 플래그 저장 또는 갱신
            obj, created = AuthInfo.objects.get_or_create(
                challenge_name=gamebox.challenge_name,
                team_id=gamebox.team_id,
                challenge_id=gamebox.challenge_id,
                round=rounds,
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
    action_tries = ActionTry.objects.filter(attacker_name=team_name, round=round)
    data = serializers.serialize('json', action_tries)
    return JsonResponse(data, safe=False)

