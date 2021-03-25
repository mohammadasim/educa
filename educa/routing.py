"""
Channels expects you to define a single root application that will be
executed for all requests. You can define the root application by adding
the ASGI_APPLICATION setting to your project. This is similar to the
ROOT_URLCONF setting that points to the base URL patterns of your project.
You can also place the root application anywhere in your project, but it
is recommended to put it in a project-level file named routing.py
"""

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

import chat.routing


# We use the ProtocolTypeRouter class provided by Channels as the
# main entry point of your routing system.
# ProtocolTypeRouter takes a dictionary that maps communication
# types like http or websocket to ASGI applications.
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
