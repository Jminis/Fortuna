from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def login_view(request):
    if request.method == 'POST':
        team_name = request.POST['name']
        password = request.POST['password']
        team = authenticate(request, name=team_name, password=password)
        if team is not None:
            login(request, team)
            return redirect('index')
    return render(request, 'account/login.html')

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