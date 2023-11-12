import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected!")
        # Joining the "chat" group
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leaving the "chat" group
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['data']

        from .models import log_Message
        message = log_Message(content=message_content)
        message.save()

        # No need to send a message to the group here because it's handled by the post_save signal.

    async def chat_message(self, event):
        message = event['message']

        # Send a message to WebSocket
        await self.send(text_data=json.dumps({
            'data': message
        }))

