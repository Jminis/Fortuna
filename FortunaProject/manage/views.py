from django.shortcuts import render
from django.utils import timezone
from config.models import Config
from datetime import timedelta
from django.conf import settings
import os

# Create your views here.
def manage_home_view(request):
    context = {}
    return render(request, 'manage/manage_home.html', context)

def manage_challenge_view(request):
    context = {}
    return render(request, 'challenge/manage_challenge.html', context)


def dashboard_view(request):
    # 현재 대회 설정 불러오기
    current_config = Config.objects.first()
    
    # 현재 시간
    now = timezone.now()
    
    # 현재 라운드 계산
    if current_config:
        round_duration = timedelta(minutes=current_config.round_time)
        elapsed_time = now - current_config.starttime
        current_round = int(elapsed_time / round_duration) + 1
        total_rounds = int((current_config.endtime - current_config.starttime) / round_duration)
        rounds_left = total_rounds - current_round
    else:
        current_round = 0
        rounds_left = 0
        total_rounds = 0
    
    # Gamebox 상태 (실제 상태는 모델에서 가져와야 함, 여기서는 예시)
    gamebox_status = {
        'A-team': ['inactive', 'active', 'inactive'],
        'B-team': ['active', 'inactive', 'active'],
        'C-team': ['active', 'active', 'active']
    }
    
    # Django 로그 파일 읽기
    log_file_path = os.path.join('./', 'django.log')
    try:
        with open(log_file_path, 'rb') as file:  # Open the file in binary mode
            django_log = tail(file, lines=100)  # Call the adjusted tail function
    except FileNotFoundError:
        django_log = "Log file not found."
    
    context = {
        'current_config': current_config,
        'current_time': now.strftime('%H:%M'),
        'current_round': current_round,
        'rounds_left': rounds_left,
        'total_rounds': total_rounds,
        'gamebox_status': gamebox_status,
        'django_log': django_log,
    }
    
    return render(request, 'manage/dashboard.html', context)


def tail(f, lines=20):
    """Read the last 'lines' lines from file 'f'."""
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)  # Move the cursor to the end of the file
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0, 0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')  # Count the newlines in binary mode
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))  # Join using binary mode
    return all_read_text.decode('utf-8').splitlines()[-total_lines_wanted:]  # Decode and split lines
