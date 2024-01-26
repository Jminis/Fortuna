import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ActionLog
from .models import ActionTry
from challenge.models import GameBox
from account.models import Team
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

    #플래그 체크, 점수/is_attacked 갱신, 로그 생성
    async def check_flag_and_create_log(self, flag):
        user = self.scope['user']
        correct = False  # 초기값을 False로 설정

        # Asynchronously find a matching AuthInfo and create an ActionLog
        try:
            auth_info = await database_sync_to_async(AuthInfo.objects.get)(flag=flag)
            correct = True  # 일치하는 flag가 있을 경우 correct를 True로 설정

            # 이미 제출된 플래그인지 확인
            existing_log = await database_sync_to_async(self.check_existing_action_log)(
                auth_info.team_id, 
                auth_info.challenge_id, 
                user,
                auth_info.round
            )
            # 이미 제출된 플래그일 경우
            if existing_log:
                await self.send(text_data=json.dumps({'toast': "이미 제출된 플래그입니다!"}))
                correct = False
                return

            await self.send(text_data=json.dumps({'toast': f"You've been attacked {auth_info.team_id}"}))

            #사용자 입력 로그 갱신
            await database_sync_to_async(self.create_action_try)(user, flag, correct)

            #correct가 True인 경우에만 is_attacked와 score, actionlog 갱신
            if correct == True:
                # is_attacked 갱신
                score = await database_sync_to_async(self.update_game_box)(auth_info.team_id, auth_info.challenge_id)
                # score 갱신
                await database_sync_to_async(self.update_team_score)(auth_info.team_id, score)

                #공격 로그(actionlog) 생성
######################라운드 일괄 1 설정
                round = 1                
                await database_sync_to_async(self.create_action_log)(auth_info, flag, round)
                return f"{auth_info.team_id} is attacked by {user}"  # user를 사용해 사용자 이름을 반환
        except AuthInfo.DoesNotExist:
            await self.send(text_data=json.dumps({'toast': f"Sent: {flag}"}))
            await database_sync_to_async(self.create_action_try)(user, flag, correct)  # Incorrect 플래그에 대한 ActionTry 생성


    def create_action_log(self, auth_info, flag, round):
######################################
        user = self.scope['user']   #attacker_team_id로 user id를 쓰고 있음. 로그인이 team_name으로 됨
        ActionLog.objects.create(
            #name=auth_info.name,
            team_id=auth_info.team_id,
            challenge_id=auth_info.challenge_id,
            attacker_team_id=user,
            round=round
        )

    def create_action_try(self, submit_team, contents, correct):
        user = self.scope['user']   #attacker_team_id로 user id를 쓰고 있음. 로그인이 team_name으로 됨
        ActionTry.objects.create(
            submit_team=submit_team,
            contents=contents,
            correct=correct,
            attacker_team_id=user
        )

    def update_game_box(self, team_id, challenge_id):
        game_boxes = GameBox.objects.filter(team_id=team_id, challenge_id=challenge_id)
        scores = []
        for game_box in game_boxes:
            game_box.is_attacked = True
            game_box.save()
            scores.append(game_box.score)
        return scores[0]


    def update_team_score(self, team_id, score_to_deduct):
        print("here's update team score")
        try:
            teams = Team.objects.filter(team_id=team_id)
            print(f"teams: {teams}")
            if teams.count() == 1:
                team = teams.first()
                print(f"team is {team}")
                team.score -= score_to_deduct
                team.save()
        except Team.DoesNotExist:
            print("Team doesn't exist")
            pass  # 혹은 적절한 로깅 또는 예외 처리


    def check_existing_action_log(self, team_id, challenge_id, attacker_team_id, round):
        return ActionLog.objects.filter(
            team_id=team_id, 
            challenge_id=challenge_id, 
            attacker_team_id=attacker_team_id, 
########################라운드 일괄 1            
            round=1
            #round=round
        ).exists()


