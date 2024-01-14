from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Notices
from .forms import NoticeForm

def notice_view(request):
    notices = Notices.objects.all()
    return render(request, 'notice/notice.html', {'notices': notices})

@login_required
def create_notice_view(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_notice')
    else:
        form = NoticeForm()
    return render(request, 'notice/create_notice.html', {'form': form})
