# adminpage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home_view, name='admin_home'),
    path('challenge', views.admin_challenge_view, name='admin_challenge'),
    # 추가 URL 패턴들...
]
