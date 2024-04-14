from django.shortcuts import render, redirect
from .models import Config
from .forms import ConfigForm
from challenge.models import GameBox
import json
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from datetime import timedelta

from functools import wraps
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
def config_view(request):
    #config 입력
    if request.method == "POST":
        form = ConfigForm(request.POST)
        if form.is_valid():
            config = form.save()

            PeriodicTask.objects.all().delete()
            IntervalSchedule.objects.all().delete()
            CrontabSchedule.objects.all().delete()

            total_time = config.endtime - config.starttime
            round_duration = config.round_time * 60  # Convert minutes to seconds
            rounds = int(total_time.total_seconds() // round_duration)

            first_run_time = config.starttime + timedelta(minutes=config.round_time)

            interval_schedule, created = IntervalSchedule.objects.get_or_create(
                every=config.round_time,
                period=IntervalSchedule.MINUTES,
            )

            PeriodicTask.objects.create(
                interval=interval_schedule, 
                name=f'Round Tasks for {config.ctf_name}',
                task='config.tasks.reset_gamebox_attack_status',
                start_time=first_run_time,  # 최초 실행 시간
            )

            return redirect('config')  # 성공적으로 저장 후 같은 뷰로 리디렉션
    else:
        form = ConfigForm()  # GET 요청 시 빈 폼 생성    
    
    #config 가져오기
    try:
        config = Config.objects.latest('created_at')
        context = {'config': config, 'form': form}
    except Config.DoesNotExist:
        context = {'form': form}  # Config 데이터가 없을 경우 form만 컨텍스트에 추가

    return render(request, 'config/config.html', context)


