from django.http import JsonResponse
from django.utils import timezone
from account.models import Team

def rank_view(request):
    teams = Team.objects.all().order_by('-score')
    data = [{'name': team.name, 'score': team.score, 'rank': idx + 1} for idx, team in enumerate(teams)]
    server_time = timezone.now()
    return JsonResponse({'teams': data, 'server_time': server_time.isoformat()}, safe=False)
