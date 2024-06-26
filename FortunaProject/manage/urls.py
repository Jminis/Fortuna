# manage/urls.py

from django.urls import path
from . import views

from account import views as account
from notice import views as notice
from flag import views as flag 
from challenge import views as challenge
from config import views as config

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Team
    path('team/', account.manage_team_view, name='manage_team'),
    path('delete_team/<int:team_id>', account.delete_team_view, name='delete_team'),
    path('update_team/<int:team_id>', account.update_team_view, name='update_team'),

    # Notice
    path('notice/', notice.manage_notice_view, name='manage_notice'),
    path('delete_notice/<int:notice_id>', notice.delete_notice_view, name='delete_notice'),


    # Challenge
    path('challenge/', challenge.manage_gamebox_view, name='manage_challenge'),
    path('upsert_challenge/', challenge.upsert_challenge_view, name='upsert_challenge'),

    # Flag
    path('flag/', flag.flag_view, name='flag'),
    path('flag/create_flag/', flag.create_flag_view, name='create_flag'),
    path('flag/export_authinfo/', flag.export_authinfo_to_txt, name='export_authinfo'),
    path('flag/chall_round_view', flag.flag_view, name='flag_view'),
    path('create_one_flag/<int:team_id>/<int:challenge_id>/', flag.create_one_flag, name='create_one_flag'),
    path('get_action_tries/<str:team_name>/', flag.get_action_tries_for_team, name='get_action_tries_for_team'),

    # Config
    path('config/', config.config_view, name='config'),
]

