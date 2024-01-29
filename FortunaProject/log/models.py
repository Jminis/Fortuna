from django.db import models

class ActionLog(models.Model):
    attacker_name = models.CharField(max_length=50)
    attacked_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    attacked_team_id = models.PositiveIntegerField(null=True, blank=True)
    challenge_id = models.PositiveIntegerField(null=True, blank=True)
    game_box_id = models.PositiveIntegerField(null=True, blank=True)
    attacker_team_id = models.PositiveIntegerField(null=True, blank=True)
    round = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'action_log'

class ActionTry(models.Model):
    attacker_name = models.CharField(max_length=50)
    contents = models.TextField()
    correct = models.BooleanField()
    attacker_team_id = models.PositiveIntegerField(null=True, blank=True)
    round = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.attacker_name} - {'Correct' if self.correct else 'Incorrect'}"
