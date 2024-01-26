from django.db import models

class Config(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    ctf_name = models.TextField()
    flag_head = models.TextField()
    round_time = models.IntegerField()
    point_down = models.IntegerField()
    point_attack = models.IntegerField()
    point_base = models.IntegerField()
    db_name = models.TextField()
    db_port = models.IntegerField()
    db_username = models.TextField()
    db_password = models.TextField()

    def __str__(self):
        return self.ctf_name
    
    def save(self, *args, **kwargs):
        # Config 테이블에 이미 데이터가 존재한다면, 기존 레코드를 업데이트
        if Config.objects.exists():
            # id=1 또는 첫 번째 레코드를 가져와 업데이트
            config = Config.objects.first()
            config.__dict__.update(self.__dict__)
            config.save(update_fields=[field.name for field in self._meta.fields])
        else:
            # 아직 데이터가 없는 경우, 새 레코드를 생성
            super(Config, self).save(*args, **kwargs)