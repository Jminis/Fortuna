from django.shortcuts import render

# Create your views here.
def manage_home_view(request):
    context = {}
    return render(request, 'manage/manage_home.html', context)

def manage_challenge_view(request):
    context = {}
    return render(request, 'challenge/manage_challenge.html', context)
