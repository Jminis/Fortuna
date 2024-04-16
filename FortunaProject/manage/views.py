from django.shortcuts import render, redirect
from django.utils import timezone
from config.models import Config
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from functools import wraps
import os

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
@login_required
def manage_challenge_view(request):
    context = {}
    return render(request, 'challenge/manage_challenge.html', context)

import paramiko
from challenge.models import GameBox

@admin_required
@login_required
def dashboard_view(request):
    timezone.activate('Asia/Seoul')
    current_config = Config.objects.latest('created_at')
    now = timezone.localtime(timezone.now())
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

    # Initialize gamebox status dictionary
    gamebox_status = {}
    
    # Fetch all GameBoxes
    gameboxes = GameBox.objects.all()
    # Paramiko SSH client setup
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for gamebox in gameboxes:
        if gamebox.ip and gamebox.ssh_port:
            try:
                ssh.connect(gamebox.ip, port=gamebox.ssh_port, username=gamebox.ssh_user, password=gamebox.ssh_password, timeout=5)
                status = 'active'
            except Exception as e:
                status = 'inactive'
            finally:
                ssh.close()

            # Update gamebox status, grouping by team_id
            if gamebox.team_id in gamebox_status:
                gamebox_status[gamebox.team_id].append(status)
            else:
                gamebox_status[gamebox.team_id] = [status]
    
    
    # Django 로그 파일 읽기
    log_file_path = os.path.join('./', 'django.log')
    try:
        with open(log_file_path, 'rb') as file:  # Open the file in binary mode
            django_log = tail(file, lines=100)  # Call the adjusted tail function
    except FileNotFoundError:
        django_log = "Log file not found."

    gamebox_status_list = {team: statuses for team, statuses in gamebox_status.items()}
    max_gameboxes = max([len(statuses) for statuses in gamebox_status.values()], default=0)
    status_headers = range(1, max_gameboxes + 1)

    context = {
        'current_config': current_config,
        'current_time': now.strftime('%H:%M'),
        'current_round': current_round,
        'rounds_left': rounds_left,
        'total_rounds': total_rounds,
        'status_headers': status_headers,
        'gamebox_status': gamebox_status_list,
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
