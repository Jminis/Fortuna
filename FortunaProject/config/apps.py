from django.apps import AppConfig
import threading

# class ConfigConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'config'

#     def ready(self):
#         from .tasks import check_and_manage_project_status
#         if threading.current_thread() == threading.main_thread():
#             thread = threading.Thread(target=check_and_manage_project_status)
#             thread.daemon = True  # 이 스레드가 메인 프로그램이 종료될 때 자동으로 종료되도록 설정
#             thread.start()
