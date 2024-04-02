from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notices
from .forms import NoticeForm

def notice_view(request):
    notices = Notices.objects.all()
    return render(request, 'notice/notice.html', {'notices': notices})

@login_required
def manage_notice_view(request):
    notices = Notices.objects.all()  # 공지사항 목록 불러오기

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_notice')
    else:
        form = NoticeForm()

    return render(request, 'notice/manage_notice.html', {'form': form, 'notices': notices})


@login_required
def delete_notice_view(request, notice_id):
    if request.method == 'POST':
        notice = get_object_or_404(Notices, id=notice_id)
        notice.delete()
    return redirect('manage_notice')