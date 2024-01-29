#challenge/models.py
from django.db import models
from account.models import Team # Account - Team 모델 / 유저 정보 가져오기

class GameBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    challenge_id = models.PositiveIntegerField(null=True, blank=True)
    challenge_name = models.CharField(max_length=255, null=True, blank=True)
    team_id = models.PositiveIntegerField(null=True, blank=True)
    ip = models.CharField(max_length=255, null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    ssh_port = models.PositiveIntegerField(null=True, blank=True)
    ssh_user = models.CharField(max_length=255, null=True, blank=True)
    ssh_password = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    visible = models.BooleanField(null=False, blank=True, default=True)
    score = models.FloatField(null=True, blank=True)
    is_down = models.BooleanField(null=False, blank=True, default=False)
    is_attacked = models.BooleanField(null=False, blank=True, default=False)

    class Meta:
        db_table = 'game_boxes'