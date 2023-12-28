from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.notice_view, name='notice'),
]