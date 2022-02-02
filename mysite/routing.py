from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path( 'ws/briefSNS/dm/<str:name1>/<str:name2>/', consumers.ChatConsumer.as_asgi() ),
]