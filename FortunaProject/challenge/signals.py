# challenge/signals.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from .models import GameBox

@receiver(post_save, sender=GameBox)
def gamebox_post_save(sender, instance, created, **kwargs):
    if created: # 데이터 인스턴스 생성에 대한 시그널
        pass
    else: # 데이터 인스턴스 업데이트에 대한 시그널
        previous_instance = GameBox.objects.get(id=instance.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "challenge_group",  # 웹소켓 그룹 이름
            {
                "type": "challenge.message",  # 호출될 컨슈머의 메서드 이름
                "text": json.dumps({
                    "team_id": instance.team_id,
                    "challenge_id": instance.challenge_id,
                    "message": "GameBox Updated"
                })
            }
        )