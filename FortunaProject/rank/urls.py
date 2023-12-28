from django.urls import path
from .views import rank_view

urlpatterns = [
    path('rank/', rank_view, name='rank'),
]