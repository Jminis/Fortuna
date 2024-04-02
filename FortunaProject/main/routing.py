from django.urls import path
from log.consumers import LogConsumer
from challenge.consumers import ChallengeConsumer
from manage.consumers import ManageConsumer

websocket_urlpatterns = [
    path('ws/log/', LogConsumer.as_asgi()),
    path('ws/challenge/', ChallengeConsumer.as_asgi()),
    path('ws/manage/', ManageConsumer.as_asgi()),
]