import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.utils.module_loading import import_string
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = ProtocolTypeRouter(
{
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
      URLRouter(
          import_string('api.routing.websocket_urlpatterns')
      )
  )
}
)
