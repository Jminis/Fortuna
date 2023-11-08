import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignupForm
import os

config_path = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

def login_view(request):
    if request.method == 'POST':
        team_name = request.POST['name']
        password = request.POST['password']
        team = authenticate(request, username=team_name, password=password)  # Change 'name' to 'username' if your user model uses 'username' field
        if team is not None:
            login(request, team)
            return redirect('index')  # Ensure you have 'index' view or URL configured in your urls.py
        else:
            # It's good to give some feedback when login fails
            context = {
                'error': "Invalid team name or password.",
                'config': config_data['login'],
            }
            return render(request, 'account/login.html', context)
    else:
        context = {
            'config': config_data['login'],
        }
        return render(request, 'account/login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')
