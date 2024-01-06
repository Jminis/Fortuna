# adminpage/urls.py

from django.urls import path
from . import views
from account import views as account

urlpatterns = [
    path('', views.admin_home_view, name='admin_home'),
    path('create/', account.create_team_view, name='create_team'),
    # 추가 URL 패턴들...
]
