#challenge/models.py
from django.db import models
from account.models import Team # Account - Team 모델 / 유저 정보 가져오기

class GameBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)         ## 생성 시간
    challenge_id = models.PositiveIntegerField(null=True, blank=True)                   ## 식별자
    challenge_name = models.CharField(max_length=255, null=True, blank=True)            ## 챌린지 이름
    description = models.CharField(max_length=500, null=True, blank=True)               ## 챌린지 설명
    visible = models.BooleanField(null=False, blank=True, default=True)                 ## 챌린지 가시화 여부
    score = models.FloatField(null=True, blank=True)                                    ## 챌린지 점수
    is_down = models.BooleanField(null=False, blank=True, default=False)                ## SLA 다운 여부
    is_attacked = models.BooleanField(null=False, blank=True, default=False)            ## 공격 받은 여부
    team_id = models.PositiveIntegerField(null=True, blank=True)                        ## 챌린지 소유 팀 식별자

    class Meta:
        db_table = 'game_boxes'

class Challenge(models.Model):
    team_id = models.PositiveIntegerField(null=True, blank=True)                        ## 챌린지 소유 팀 식별자
    ip = models.CharField(max_length=255, null=True, blank=True)                        ## IP 주소
    port = models.PositiveIntegerField(null=True, blank=True)                           ## 포트 번호
    ssh_port = models.PositiveIntegerField(null=True, blank=True)                       ## SSH 포트 번호
    ssh_user = models.CharField(max_length=255, null=True, blank=True)                  ## SSH 사용자 이름
    ssh_password = models.CharField(max_length=255, null=True, blank=True)              ## SSH 비밀번호
    
    class Meta:
        db_table = 'challenges'
