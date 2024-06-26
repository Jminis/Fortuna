from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_view, name='challenge'),
    path('get_challenge_data',views.get_gamebox_data, name='get_challenge_data'),
    path('update_gamebox_status',views.update_gamebox_status, name='update_gamebox_status'),
]
