# challenge/routing.py
from django.urls import re_path
from .consumers import ChallengeConsumer

websocket_urlpatterns = [
    re_path(r'ws/challenge/$', ChallengeConsumer.as_asgi()),
]