from django.urls import path
from log.consumers import LogConsumer
<<<<<<< HEAD
from challenge.consumers import ChallengeConsumer

websocket_urlpatterns = [
    path('ws/log/', LogConsumer.as_asgi()),
    path('ws/challenge/', ChallengeConsumer.as_asgi()),
=======

websocket_urlpatterns = [
    path('ws/log/', LogConsumer.as_asgi()),
>>>>>>> main
]