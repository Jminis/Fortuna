from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_view, name='challenge'),
    path('data/', views.test_data),
    path('get_data',views.get_gamebox_data),
]
