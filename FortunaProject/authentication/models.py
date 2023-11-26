from django.db import models

class AuthInfo(models.Model):
    team_id = models.PositiveIntegerField(null=True, blank=True)
    challenge_id = models.IntegerField()
    round = models.IntegerField()
    flag = models.TextField()

    def __str__(self):
        return f"Team ID: {self.team_id}, Challenge ID: {self.challenge_id}"
