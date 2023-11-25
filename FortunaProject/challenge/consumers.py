# challenge/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChallengeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Challegne WebSocket connected!")
        # Joining the "chat" group
        await self.channel_layer.group_add("challenge_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leaving the "chat" group
        await self.channel_layer.group_discard("challenge_group", self.channel_name)

    # 시그널로부터 메시지를 받아 클라이언트에 전송
    async def challenge_message(self, event):
        message = event["text"]
        await self.send(text_data=message)
