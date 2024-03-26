import json
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TeamCreationForm
from .models import Team
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

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
@admin_required
def manage_team_view(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.set_password(form.cleaned_data['password'])
            team.save()
            messages.success(request, 'Team created successfully!')
            return redirect('manage_team')
    else:
        form = TeamCreationForm()

    teams = Team.objects.all()
    return render(request, 'account/manage_team.html', {'form': form, 'teams': teams})

@login_required
@admin_required
def delete_team_view(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        if team.is_superuser or team.is_staff:
            messages.error(request, "Cannot delete an admin account.")
            return redirect('manage_team')
        
        team.delete()
        messages.success(request, 'Team deleted successfully.')
    except Team.DoesNotExist:
        messages.error(request, 'Team not found.')
    return redirect('manage_team')

@login_required
@admin_required
def update_team_view(request, team_id):
    
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        messages.error(request, 'Team not found.')
        return redirect('manage_team')

    if request.method == 'POST':
        form = TeamCreationForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.set_password(form.cleaned_data['password'])
            team.save()
            messages.success(request, 'Team updated successfully!')
            return redirect('manage_team')
    else:
        form = TeamCreationForm(instance=team)

    return render(request, 'account/manage_team.html', {'form': form, 'team_id': team_id})

def logout_view(request):
    logout(request)
    return redirect('/')