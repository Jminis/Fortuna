from django.urls import path
from log.consumers import LogConsumer
from rank.consumers import RankConsumer

websocket_urlpatterns = [
    path('ws/log/', LogConsumer.as_asgi()),
    path('ws/rank/', RankConsumer.as_asgi()),
]