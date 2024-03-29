from django.db import models

class AuthInfo(models.Model):
    challenge_name = models.CharField(max_length=255, null=True)
    team_id = models.PositiveIntegerField(null=True, blank=True)
    challenge_id = models.IntegerField()
    round = models.IntegerField()
    flag = models.TextField()
    team_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Team ID: {self.team_id}, Challenge ID: {self.challenge_id}"
