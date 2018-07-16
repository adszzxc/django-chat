from channels.routing import ProtocolTypeRouter
from django.urls import path
from api.consumers import ChatConsumer
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
#### Token authentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):    
        path = scope["path"]
        token_key = path.split('/')[4]
        try:
            token = Token.objects.get(key=token_key)
            scope['user'] = token.user
        except Token.DoesNotExist:
            scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
                

#### rest of the code:

application = ProtocolTypeRouter({
    "websocket":TokenAuthMiddlewareStack(
        URLRouter([
            path("ws/usercode/<str:usercode>/<str:authtoken>/", ChatConsumer),
            ]),
        ),
    })
