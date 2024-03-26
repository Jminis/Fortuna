from django.http import JsonResponse
from django.utils import timezone
from account.models import Team

def rank_view(request):
    teams = Team.objects.filter(team_id__isnull=False).order_by('-score')
    data = [{'name': team.name, 'score': team.score, 'rank': idx + 1} for idx, team in enumerate(teams)]
    server_time = timezone.now()

    # 로그인한 사용자의 이름을 확인합니다. 로그인하지 않은 경우 None을 사용합니다.
    login_team_name = request.user.name if request.user.is_authenticated else None
    

    return JsonResponse({'teams': data, 'server_time': server_time.isoformat(), 'login_team_name': login_team_name}, safe=False)
