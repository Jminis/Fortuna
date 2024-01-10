# manager/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_home_view, name='manager_home'),
    path('challenge', views.manager_challenge_view, name='manager_challenge'),
    # 추가 URL 패턴들...
]
