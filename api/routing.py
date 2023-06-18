from django.urls import re_path
from .consumers import ChatConsumer
from .urls import urlpatterns
websocket_urlpatterns = [
    re_path(r'ws/conversation/$', ChatConsumer.as_asgi()),
    # re_path(r'ws/conversation/$', ConversationConsumer.as_asgi()),
]

