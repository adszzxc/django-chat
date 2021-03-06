from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync



class ChatConsumer(JsonWebsocketConsumer):   
    def connect(self):
        self.accept()
        self.usercode = self.scope["url_route"]["kwargs"]["usercode"]
        async_to_sync(self.channel_layer.group_add)(str(self.usercode), self.channel_name)
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(str(self.usercode), self.channel_name)
    def chat_message(self, event):
        self.send_json(content=event)
