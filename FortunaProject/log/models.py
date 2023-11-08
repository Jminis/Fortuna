from django.db import models

# Create your models here.

class log_Message(models.Model):
    content = models.TextField()

