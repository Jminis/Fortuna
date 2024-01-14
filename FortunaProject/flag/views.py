from django.shortcuts import render
import hashlib
import secrets
from challenge.models import GameBox
from authentication.models import AuthInfo
from django.http import HttpResponseRedirect
from django.urls import reverse

def flag_view(request):
    flags = AuthInfo.objects.all()  # 모든 AuthInfo 인스턴스를 가져옵니다.
    return render(request, 'flag/flag.html', {'flags': flags})


def create_flag():
    for challenge in GameBox.objects.values_list('challenge_id', flat=True).distinct():
        round_info = get_round_info()  # 라운드 정보를 가져오는 함수(예시)
        salt = secrets.token_hex(8)
        raw_flag = f"{round_info}{challenge}{salt}"

        hashed_flag = hashlib.sha256(raw_flag.encode()).hexdigest()
        final_flag = f"SF{{{hashed_flag}}}"

        # AuthInfo 모델의 해당 challenge_id를 가진 모든 인스턴스에 플래그 저장
        AuthInfo.objects.filter(challenge_id=challenge).update(flag=final_flag)

    return "Flags created and updated in AuthInfo for all challenge IDs"

def create_flag_view(request):
    create_flag()  # 플래그 생성
    return HttpResponseRedirect(reverse('flag'))  # 플래그 관리 페이지로 리다이렉트

def get_round_info():
    # 라운드 정보를 반환하는 함수
    # 이 부분은 라운드 정보를 어떻게 관리하는지에 따라 달라집니다.
    pass

