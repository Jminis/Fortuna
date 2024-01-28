# manage/urls.py

from django.urls import path
from . import views

from account import views as account
from notice import views as notice
from flag import views as flag 
from challenge import views as challenge
from config import views as config

urlpatterns = [
    path('', views.manage_home_view, name='manage_home'),

    # Team
    path('team/', account.manage_team_view, name='manage_team'),
    path('delete/<int:team_id>/', account.delete_team_view, name='delete_team'),
    path('update/<int:team_id>/', account.update_team_view, name='update_team'),

    # Notice
    path('notice/', notice.create_notice_view, name='create_notice'),

    # Challenge
    path('challenge/', challenge.manage_gamebox_view, name='manage_challenge'),
    path('delete_challenge/<int:id>/', challenge.delete_gamebox_view, name='delete_challenge'),
    path('update_challenge/<int:id>/', challenge.update_gamebox_view, name='update_challenge'),

    # Flag
    path('flag/', flag.flag_view, name='flag'),
    path('flag/create_flag/', flag.create_flag_view, name='create_flag'),

    # Config
    path('config/', config.config_view, name='config'),
]

