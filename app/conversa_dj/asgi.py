import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conversa_dj.settings")



from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip
from . import routing  # noqa isort:skip
from channels.security.websocket import AllowedHostsOriginValidator  # noqa isort:skip
from chats.middleware import TokenAuthMiddleware  # noqa isort:skip


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(routing.websocket_urlpatterns),
            )
        )
    }
)
