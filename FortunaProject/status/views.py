from django.shortcuts import render
from itertools import groupby
from operator import attrgetter

def status_view(request):
    from challenge.models import GameBox
    game_boxes = GameBox.objects.all().order_by('team_id', 'challenge_id')

    grouped_game_boxes = {}
    for team_id, boxes in groupby(game_boxes, key=attrgetter('team_id')):
        grouped_game_boxes[team_id] = [
            {
                'challenge_id': box.challenge_id,
                'is_down': box.is_down,
                'is_attacked': box.is_attacked,
                # 추가로 필요한 필드를 여기에 포함시킬 수 있습니다.
            }
            for box in boxes
        ]
    return render(request, 'status/status.html', {'grouped_game_boxes': grouped_game_boxes})
