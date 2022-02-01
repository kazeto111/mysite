from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path( 'ws/briefSNS/dm/', consumers.ChatConsumer.as_asgi() ),
]