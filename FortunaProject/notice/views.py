from django.shortcuts import render
from .models import Notices

def notice_view(request):
    notices = Notices.objects.all()
    return render(request, 'notice/notice.html', {'notices': notices})
