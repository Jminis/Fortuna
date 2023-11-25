from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('play/', views.play_view, name='play'),
    path('',include('rank.urls'), name='rank'), #이거 빼면 /rank로 접근 못함
    path('',include('log.urls'), name='log'), 
]