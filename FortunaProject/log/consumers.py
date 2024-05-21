import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ActionLog
from .models import ActionTry
from challenge.models import GameBox
from account.models import Team
from authentication.models import AuthInfo
from config.models import Config
from django.utils import timezone
import logging
from django.db import IntegrityError

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

    @database_sync_to_async
    def get_latest_config(self):
        try:
            return Config.objects.latest('created_at')
        except Config.DoesNotExist:
            return None

    async def calculate_current_round(self):
        config = await self.get_latest_config()
        if config:
            now = timezone.localtime()
            elapsed_time = now - timezone.localtime(config.starttime)
            total_minutes = int(elapsed_time.total_seconds() // 60)
            current_round = total_minutes // config.round_time
            return current_round
        else:
            return 1  # Default round value if no config is found


    #플래그 체크, 점수/is_attacked 갱신, 로그 생성
    async def check_flag_and_create_log(self, flag):
        user = self.scope['user']
        correct = False  # 초기값을 False로 설정
        team = await database_sync_to_async(Team.objects.get)(name=user)
        attacker_team_id = team.team_id

        round = await self.calculate_current_round()

        try:
            auth_info = await database_sync_to_async(AuthInfo.objects.get)(flag=flag, round=round)
            correct = True  # 일치하는 flag가 있을 경우 correct를 True로 설정

            # 이미 제출된 플래그인지 확인
            existing_log = await database_sync_to_async(self.check_existing_action_log)(
                auth_info.team_id, 
                auth_info.challenge_id, 
                attacker_team_id,
                round
            )
            # 이미 제출된 플래그일 경우
            if existing_log:
                await self.send(text_data=json.dumps({'toast': "이미 제출된 플래그입니다."}))
                correct = False
                return

            #같은 팀을 공격한 경우
            if auth_info.team_name == str(user):
                await self.send(text_data=json.dumps({'toast': "다른 팀을 공격해주세요."}))
                correct = False
                return

            await self.send(text_data=json.dumps({'toast': f"{auth_info.team_name}팀을 공격했습니다."}))

            #사용자 입력 로그 갱신
            await database_sync_to_async(self.create_action_try)(user, flag, correct, attacker_team_id, round)

            #correct가 True인 경우에만 is_attacked와 score, actionlog 갱신
            if correct == True:
                # is_attacked 갱신
                point_down, point_up = await database_sync_to_async(self.update_game_box)(auth_info.team_id, auth_info.challenge_id)
                # score 갱신
                await database_sync_to_async(self.update_team_score)(auth_info.team_id, point_down, attacker_team_id, point_up)

                #공격 로그(actionlog) 생성                
                await database_sync_to_async(self.create_action_log)(user, auth_info, flag, round, attacker_team_id)
                return f"{auth_info.team_name} is attacked by {user}"
        except AuthInfo.DoesNotExist:
            await self.send(text_data=json.dumps({'toast': f"Sent: {flag}"}))
            await database_sync_to_async(self.create_action_try)(user, flag, correct, attacker_team_id, round)  # Incorrect 플래그에 대한 ActionTry 생성

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    def create_action_log(self, user, auth_info, flag, round, attacker_team_id):
        # 로그 기록: Action 로그 생성 시작
        logging.info(f"Creating action log: Attacker={user}, Attacked={auth_info.team_name}, Round={round}")
        
        ActionLog.objects.create(
            attacker_name=user,
            attacked_name=auth_info.team_name,
            attacked_team_id=auth_info.team_id,
            attacker_team_id=attacker_team_id,
            challenge_id=auth_info.challenge_id,
            round=round
        )
        # 로그 기록: Action 로그 생성 완료
        logging.info(f"Action log created successfully for round {round}")

    def create_action_try(self, user, contents, correct, attacker_team_id, round):
        ActionTry.objects.create(
            attacker_name = user,
            contents=contents,
            correct=correct,
            attacker_team_id=attacker_team_id,
            round=round
        )

    def update_game_box(self, team_id, challenge_id):
        game_boxes = GameBox.objects.filter(team_id=team_id, challenge_id=challenge_id)
        scores = []
        for game_box in game_boxes:
            game_box.is_attacked = True
            game_box.save()
            scores.append(game_box.point_down)
            scores.append(game_box.point_attack)
        return scores[0], scores[1]


    def update_team_score(self, attacked_id, score_to_deduct, attacker_id, score_to_plus):
        #점수 차감
        try:
            teams = Team.objects.filter(team_id=attacked_id)
            if teams.count() == 1:
                team = teams.first()
                team.score -= score_to_deduct
                team.save()
        except Team.DoesNotExist:
            print("Team doesn't exist")
            pass  # 혹은 적절한 로깅 또는 예외 처리
        #점수 차증
        try:
            teams = Team.objects.filter(team_id=attacker_id)
            if teams.count() == 1:
                team = teams.first()
                team.score += score_to_plus
                team.save()
        except Team.DoesNotExist:
            print("Team doesn't exist")
            pass  # 혹은 적절한 로깅 또는 예외 처리


    def check_existing_action_log(self, team_id, challenge_id, attacker_team_id, round):
        return ActionLog.objects.filter(
            attacked_team_id=team_id, 
            challenge_id=challenge_id, 
            attacker_team_id=attacker_team_id, 
            round=round
        ).exists()