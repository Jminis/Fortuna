from celery import shared_task
from challenge.models import GameBox

@shared_task
def reset_gamebox_attack_status():
    GameBox.objects.update(is_attacked=False)