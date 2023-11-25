import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ActionLog
from .models import ActionTry
from authentication.models import AuthInfo


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

        # Check if message matches any flag in AuthInfo
        response = await self.check_flag_and_create_log(message_content)

        # Only send a response back if there is one
        if response:
            await self.send(text_data=json.dumps({'data': response}))

    # async def check_flag_and_create_log(self, flag):
    #     print("checking...")
    #     user = self.scope['user']
    #     correct = False
    #     # Asynchronously find a matching AuthInfo and create an ActionLog
    #     try:
    #         auth_info = await database_sync_to_async(AuthInfo.objects.get)(flag=flag)
    #         correct = True  # 일치하는 flag가 있을 경우 correct를 True로 설정
    #         await database_sync_to_async(self.create_action_log)(auth_info, flag)
    #         return f"{auth_info.team_id} attacked by {user}"
    #     except AuthInfo.DoesNotExist:
    #         pass
        
    #     await database_sync_to_async(self.create_action_try)(user, flag, correct)


    # def create_action_log(self, auth_info, flag):
    #     user = self.scope['user']
    #     ActionLog.objects.create(
    #         team_id=auth_info.team_id,
    #         challenge_id=auth_info.challenge_id,
    #         attacker_team_id=user
    #     )

    # def create_action_try(self, submit_team, contents, correct):
    #     ActionTry.objects.create(
    #         submit_team=submit_team,
    #         contents=contents,
    #         correct=correct
    #     )

    async def check_flag_and_create_log(self, flag):
        user = self.scope['user']
        correct = False  # 초기값을 False로 설정

        # Asynchronously find a matching AuthInfo and create an ActionLog
        try:
            auth_info = await database_sync_to_async(AuthInfo.objects.get)(flag=flag)
            correct = True  # 일치하는 flag가 있을 경우 correct를 True로 설정
            await database_sync_to_async(self.create_action_try)(user, flag, correct)
            await database_sync_to_async(self.create_action_log)(auth_info, flag)
            return f"{auth_info.team_id} attacked by {user}"  # user를 사용해 사용자 이름을 반환
        except AuthInfo.DoesNotExist:
            pass
        # ActionTry 인스턴스 생성
        await database_sync_to_async(self.create_action_try)(user, flag, correct)

    def create_action_log(self, auth_info, flag):
        user = self.scope['user']
        ActionLog.objects.create(
            team_id=auth_info.team_id,
            challenge_id=auth_info.challenge_id,
            attacker_team_id=user
        )

    def create_action_try(self, submit_team, contents, correct):
        ActionTry.objects.create(
            submit_team=submit_team,
            contents=contents,
            correct=correct
        )