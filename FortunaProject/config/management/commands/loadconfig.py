from django.core.management.base import BaseCommand
import json
from django.conf import settings
import os
from config.models import Config
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Load data from config file into the database and create a new Config instance'

    def handle(self, *args, **kwargs):
        config_file_path = os.path.join(settings.BASE_DIR, 'config', 'data', 'config.json')
        
        with open(config_file_path, 'r') as file:
            data = json.load(file)
            config_instance = Config(
                starttime=parse_datetime(data['starttime']),
                endtime=parse_datetime(data['endtime']),
                ctf_name=data['ctf_name'],
                flag_head=data['flag_head'],
                round_time=data['round_time'],
                point_down=data['pointdown'],
                point_attack=data['pointattack'],
                point_base=data['pointbase'],
                db_name=data['database']['db_name'],
                db_port=data['database']['db_port'],
                db_username=data['database']['db_username'],
                db_password=data['database']['db_password'],
            )
            config_instance.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created new Config instance with ID {config_instance.id}'))