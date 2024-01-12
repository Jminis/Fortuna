from django.shortcuts import render

# Create your views here.
def manager_home_view(request):
    context = {}
    return render(request, 'manager/manager_home.html', context)

def manager_challenge_view(request):
    context = {}
    return render(request, 'manager/manager_challenge.html', context)
