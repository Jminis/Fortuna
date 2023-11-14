from django.urls import path
from . import views

urlpatterns = [
    path('challenge/', views.challenge_view, name='challenge'),
    path('challenge/data/', views.test_data),
    path('challenge/get_data',views.get_gamebox_data),
]
