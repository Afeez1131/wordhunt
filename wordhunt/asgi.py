"""
ASGI config for wordhunt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from core import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordhunt.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([re_path('ws/home/', consumers.WordHuntConsumer.as_asgi())])
    )
})

