from django.shortcuts import render
from account.models import Team  # 'account' 앱에서 'Team' 모델을 임포트


def rank_view(request):
    teams = Team.objects.all().order_by('-score')  # 점수가 높은 순으로 팀들을 정렬
    context = {'teams': teams}
    return render(request, 'rank.html', context)  # rank.html 템플릿으로 데이터 전달
