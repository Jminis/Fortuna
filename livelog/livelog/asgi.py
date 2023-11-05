import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import log.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livelog.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(log.routing.websocket_urlpatterns)
})

