from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_view, name='challenge'),
<<<<<<< HEAD
    path('get_challenge_data',views.get_gamebox_data),
=======
    path('data/', views.test_data),
    path('get_data',views.get_gamebox_data),
>>>>>>> main
]
