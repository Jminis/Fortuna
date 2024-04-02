# challenge/routing.py
from django.urls import re_path
from .consumers import ManageConsumer

websocket_urlpatterns = [
    re_path(r'ws/manage/$', ManageConsumer.as_asgi()),
]