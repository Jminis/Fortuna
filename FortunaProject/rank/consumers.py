from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

class RankConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Rank WebSocket connected!")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        if message == "fetch_rank":
            # 비동기적으로 팀 데이터를 가져옵니다.
            rank_list = await self.get_ranked_teams()
            print("Sending rank data to client:", rank_list)  # 로그 추가

            # 클라이언트에 데이터를 전송합니다.
            await self.send(text_data=json.dumps({
                'message': 'rank_data',
                'data': rank_list,
            }))

    @database_sync_to_async
    def get_ranked_teams(self):
        from account.models import Team
        # 리스트 형태로 데이터를 반환합니다.
        return list(Team.objects.all().order_by('-score').values('name', 'score'))
