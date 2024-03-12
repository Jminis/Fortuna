from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve, reverse
from .models import Config

class ProjectAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 현재 시각
        now = timezone.localtime(timezone.now())
        try:
            current_url_name = resolve(request.path_info).url_name
            # 가장 최근의 Config 인스턴스를 가져옴
            latest_config = Config.objects.latest('created_at')
            # 'play/'나 'status/' URL에 대한 요청 처리
            if current_url_name in ['play', 'status_view']:
                # 현재 시간이 설정된 운영 시간 내인지 확인
                if latest_config.starttime <= now <= latest_config.endtime:
                    # 운영 시간 내이면 요청 처리를 계속 진행
                    response = self.get_response(request)
                else:
                    # 운영 시간 외이면 대회가 진행 중이지 않다는 페이지 출력해야 되는데 일단 manage로 리다이렉트
                    manage_url = reverse('not_in_progress')
                    return redirect(manage_url)
            else:
                # 다른 URL 요청은 그대로 진행
                response = self.get_response(request)
                
        except Config.DoesNotExist:
            # Config가 없는 경우, 모든 요청을 'manage/' URL로 리다이렉트
            response = self.get_response(request)

        return response
