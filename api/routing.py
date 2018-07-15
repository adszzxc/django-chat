from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/usercode/<str:usercode>/", consumers.ChatConsumer),
]
