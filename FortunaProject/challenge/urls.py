from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_view, name='challenge'),
    path('get_challenge_data',views.get_gamebox_data),
]
