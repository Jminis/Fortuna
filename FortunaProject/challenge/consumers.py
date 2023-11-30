#challenge/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChallengeConsumer(AsyncWebsocketConsumer):
    # 웹소켓 연결
    async def connect(self):
        print("Challenge WebSocket connected!")
        # Joining the "challenge_group" group
        await self.channel_layer.group_add("challenge_group", self.channel_name)
        await self.accept()

    # 웹소켓 연결 해제
    async def disconnect(self, close_code):
        # Leaving the "challenge_group" group
        await self.channel_layer.group_discard("challenge_group", self.channel_name)

    # 시그널로부터 메시지를 받아 클라이언트에 전송
    async def challenge_message(self, event):
        print('challenge_message sented!')
        message = event["text"]
        await self.send(text_data=message)
