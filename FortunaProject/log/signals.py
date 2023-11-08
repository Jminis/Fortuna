from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import log_Message

@receiver(post_save, sender=log_Message)
def announce_new_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat",
            {
                "type": "chat.message",
                "message": instance.content
            }
        )
