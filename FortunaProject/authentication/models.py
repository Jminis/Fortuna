from django.db import models

class AuthInfo(models.Model):
    team_id = models.CharField(max_length=50)
    challenge_id = models.IntegerField()
    round = models.IntegerField()
    flag = models.TextField()

    def __str__(self):
        return self.team_id
