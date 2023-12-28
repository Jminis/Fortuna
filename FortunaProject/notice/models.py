from django.db import models

class Notices(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title