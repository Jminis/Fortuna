from django.shortcuts import render
import hashlib
import secrets
from challenge.models import GameBox
from authentication.models import AuthInfo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

def flag_view(request):
    auth_info = AuthInfo.objects.all()  # 모든 AuthInfo 인스턴스를 가져옵니다.
    round = get_round_info()  # 현재 라운드 정보를 가져옵니다.
    round = 2
    round_info = AuthInfo.objects.filter(round=round)  # 현재 라운드의 AuthInfo 인스턴스를 가져옵니다.
    return render(request, 'flag/flag.html', {
        'auth_info': auth_info,
        'round': round,
        'round_info': round_info
    })

def create_one_flag(request, gamebox_id):
    # 특정 GameBox 인스턴스를 가져옵니다.
    try:
        gamebox = GameBox.objects.get(id=gamebox_id)
    except GameBox.DoesNotExist:
        # GameBox 인스턴스가 존재하지 않는 경우 오류 처리
        # 여기에 적절한 오류 메시지나 리다이렉트를 추가할 수 있습니다.
        return HttpResponse("GameBox not found", status=404)

    # 플래그 생성 로직
    round_info = get_round_info()  # 현재 라운드 정보를 가져옵니다.
    salt = secrets.token_hex(8)
    raw_flag = f"{round_info}{gamebox.challenge_id}{salt}"
    hashed_flag = hashlib.sha256(raw_flag.encode()).hexdigest()
    final_flag = f"SF{{{hashed_flag}}}"

    # AuthInfo 인스턴스에 플래그 저장 또는 갱신
    obj, created = AuthInfo.objects.get_or_create(
        challenge_name=gamebox.challenge_name,
        team_id=gamebox.team_id,
        challenge_id=gamebox.challenge_id,
        round=round_info,
        defaults={'flag': final_flag}
    )
    if not created:
        obj.flag = final_flag
        obj.save()

    # 처리 후 적절한 페이지로 리다이렉트합니다.
    return HttpResponseRedirect(reverse('flag_view'))

def create_flag():
    #rounds = Round.objects.all()  # 모든 라운드 정보를 가져옵니다
    rounds = range(1, 4)
    gameboxes = GameBox.objects.all()

    for round_info in rounds:
        for gamebox in gameboxes:
            salt = secrets.token_hex(8)
            raw_flag = f"{round_info}{gamebox.challenge_id}{salt}"
            hashed_flag = hashlib.sha256(raw_flag.encode()).hexdigest()
            final_flag = f"SF{{{hashed_flag}}}"

            obj, created = AuthInfo.objects.get_or_create(
                challenge_name=gamebox.challenge_name,
                team_id=gamebox.team_id,
                challenge_id=gamebox.challenge_id,
                round=round_info,
                defaults={'flag': final_flag}
            )
            if not created:
                obj.flag = final_flag
                obj.save()

    return "Flags created and/or updated in AuthInfo for all rounds"

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


def get_round_info():
    # 라운드 정보를 반환하는 함수
    # 이 부분은 라운드 정보를 어떻게 관리하는지에 따라 달라집니다.
    pass

