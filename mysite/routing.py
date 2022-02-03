from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path( 'briefSNS/dm/<str:name1>/<str:name2>/', consumers.ChatConsumer.as_asgi() ),
]
print("websocketパターン", websocket_urlpatterns)
print("そのタイプ", type(websocket_urlpatterns[0]))