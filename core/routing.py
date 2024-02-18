# core/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from apps.home import consumers #sume que crearás un archivo consumers.py en tu app 'home'

websocket_urlpatterns = [
    path('ws/dispositivos/', consumers.DispositivoConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})