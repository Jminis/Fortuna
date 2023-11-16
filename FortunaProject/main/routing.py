from django.urls import path
from log.consumers import LogConsumer

websocket_urlpatterns = [
    path('ws/log/', LogConsumer.as_asgi()),
]