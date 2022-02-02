"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     # その他のプロトコルもここに追加できる
# })

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#application = get_asgi_application()
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter

from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing
#セキュリティ(csrf対策)のため追加
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter( {
    'http': get_asgi_application(),
    'websocket': URLRouter( routing.websocket_urlpatterns ),
} )