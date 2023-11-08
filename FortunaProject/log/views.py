from django.http import HttpResponse
from django.shortcuts import render
from log.models import log_Message
from django.conf import settings

# Create your views here.

def log(request):
    messages = log_Message.objects.all()
    return render(request, 'log/log_.html', {'messages': messages})
