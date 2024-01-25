# manage/urls.py

from django.urls import path
from . import views
from account import views as account
from notice import views as notice
from flag import views as flag 

urlpatterns = [
    path('', views.manage_home_view, name='manage_home'),

    # Team
    path('team/', account.manage_team_view, name='manage_team'),
    path('delete_team/<int:team_id>', account.delete_team_view, name='delete_team'),
    path('update_team/<int:team_id>', account.update_team_view, name='update_team'),

    # Notice
    path('notice/', notice.create_notice_view, name='create_notice'),

    # Challenge
    path('challenge/', views.manage_challenge_view, name='manage_challenge'),

    # Flag
    path('flag/', flag.flag_view, name='flag'),
    path('flag/create_flag/', flag.create_flag_view, name='create_flag'),
]

