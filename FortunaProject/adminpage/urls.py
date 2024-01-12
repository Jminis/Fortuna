from django.urls import path
from . import views
from account import views as account_views
from admin_flag import views as admin_flag_views  # admin_flag 앱의 뷰 import

urlpatterns = [
    path('', views.admin_home_view, name='admin_home'),
    path('create/', account_views.create_team_view, name='create_team'),
    path('flag/', admin_flag_views.admin_flag_view, name='admin_flag'),
    path('flag/create_flag/', admin_flag_views.create_flag_view, name='create_flag'),
    # 기타 URL 패턴들...
]
