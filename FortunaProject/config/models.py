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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ctf_name
    
    def save(self, *args, **kwargs):
        super(Config, self).save(*args, **kwargs)

    def __str__(self):
        return self.ctf_name    