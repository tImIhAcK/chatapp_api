from django.urls import path
from chats.consumers import ChatConsumer, NotificationConsumer
from chats.consumers2 import ChatConsumer2

websocket_urlpatterns = [
    path(r"ws/<slug:conversation_name>/", ChatConsumer.as_asgi()),
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path(r'ws/chat/<str:user_id>/c/', ChatConsumer2.as_asgi())
]
