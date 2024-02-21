from django.utils import timezone
from .models import Config
import time

def start_project_tasks():
    # 프로젝트가 '실행 중'일 때 수행할 작업
    print("프로젝트 관련 작업을 시작합니다.")

def stop_project_tasks():
    # 프로젝트가 '종료 상태'에 있을 때 수행할 작업
    print("프로젝트 관련 작업을 종료합니다.")

def check_and_manage_project_status():
    project_running = False  # 프로젝트 실행 상태 플래그

    while True:
        now = timezone.now()
        try:
            latest_config = Config.objects.latest('created_at')
            if latest_config.starttime <= now <= latest_config.endtime:
                if not project_running:
                    start_project_tasks()
                    project_running = True
                print("프로젝트 실행 중...")
            else:
                if project_running:
                    stop_project_tasks()
                    project_running = False
                print("프로젝트 종료 상태 또는 대기 중...")
        except Config.DoesNotExist:
            print("설정 인스턴스가 존재하지 않습니다.")
            if project_running:
                stop_project_tasks()
                project_running = False
        time.sleep(60)  # 다음 상태 체크까지 60초 대기
