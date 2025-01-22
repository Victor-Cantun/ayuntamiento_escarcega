from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    
    #path("ws/online-status/", OnlineStatusConsumer.as_asgi()),
    #path("ws/chat-public/<room>/<id>", ChatPublic.as_asgi()),
]