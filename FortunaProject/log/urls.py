from . import views
from django.urls import path

urlpatterns = [
    path('', views.log_view)
]
