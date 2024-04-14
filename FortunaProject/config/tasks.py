from celery import shared_task
from challenge.models import GameBox

@shared_task
def reset_gamebox_attack_status():
    print("11")
    GameBox.objects.update(is_attacked=False)