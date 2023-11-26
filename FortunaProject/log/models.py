from django.db import models

class ActionLog(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    team_id = models.CharField(max_length=50)
    challenge_id = models.PositiveIntegerField(null=True, blank=True)
    game_box_id = models.PositiveIntegerField(null=True, blank=True)
    attacker_team_id = models.CharField(max_length=50)
    round = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'action_log'

class ActionTry(models.Model):
    submit_team = models.CharField(max_length=50)
    contents = models.TextField()
    correct = models.BooleanField()

    def __str__(self):
        return f"{self.submit_team} - {'Correct' if self.correct else 'Incorrect'}"
