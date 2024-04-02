import asyncio
import os
import tailer
from channels.generic.websocket import AsyncWebsocketConsumer

class ManageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.log_file_path = os.path.join('./', 'django.log')  # 로그 파일 경로 설정
        await self.accept()
        asyncio.create_task(self.send_log_updates())

    async def disconnect(self, close_code):
        # 연결 종료 시 실행될 코드
        pass

    async def send_log_updates(self):
        last_size = 0
        while True:
            await asyncio.sleep(1)  # 비동기로 일시 중지
            if os.path.exists(self.log_file_path):
                with open(self.log_file_path, 'r') as log_file:
                    log_file.seek(last_size)
                    lines = log_file.readlines()
                    last_size = log_file.tell()
                    if lines:
                        await self.send(text_data=''.join(lines))

    async def receive(self, text_data):
        # 클라이언트로부터 메시지를 받았을 때 실행될 코드
        pass
