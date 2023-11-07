from django.http import HttpResponse
from django.shortcuts import render
from log.models import log_Message


# Create your views here.

def index(request):
    messages = log_Message.objects.all()
    return render(request, 'log/index.html', {'messages': messages})
