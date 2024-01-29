import json
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import TeamCreationForm
from .models import Team
from django.template.loader import render_to_string

# Config 파일 로드
config_path = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

def login_view(request):
    if request.method == 'POST':
        team_name = request.POST.get('name')
        password = request.POST.get('password')
        
        # 입력 값 검사
        if not team_name or not password:
            messages.error(request, "Team name and password are required.")
            return redirect('login')

        team = authenticate(request, username=team_name, password=password)
        if team is not None:
            login(request, team)
            return redirect('index')
        else:
            messages.error(request, "Invalid team name or password.")
    return render(request, 'account/login.html', {'config': config_data['login']})

@login_required
def manage_team_view(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team created successfully!')
            return redirect('manage_team')
    else:
        form = TeamCreationForm()

    teams = Team.objects.all()
    return render(request, 'account/manage_team.html', {'form': form, 'teams': teams})

@login_required
def delete_team_view(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        team.delete()
        messages.success(request, 'Team deleted successfully.')
    except Team.DoesNotExist:
        messages.error(request, 'Team not found.')
    return redirect('manage_team')

@login_required
def update_team_view(request, team_id):
    
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    if request.method == 'POST':
        form = TeamCreationForm(request.POST, request.FILES, instance=team)
        print(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Team updated successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
        
@login_required
def update_team_form(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    form = TeamCreationForm(instance=team)
    # 폼을 HTML로 렌더링합니다. 이 HTML은 AJAX 요청에 대한 응답으로 사용됩니다.
    form_html = render_to_string('account/team_form.html', {'form': form}, request)
    return JsonResponse({'form_html': form_html})

def logout_view(request):
    logout(request)
    return redirect('/')