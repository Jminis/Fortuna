from django.shortcuts import render

# Create your views here.
def admin_home_view(request):
    context = {}
    return render(request, 'admin_home.html', context)

def admin_challenge_view(request):
    context = {}
    return render(request, 'admin_challenge.html', context)
