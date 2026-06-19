from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Get the recipient (the other person in the conversation)
        recipient = instance.conversation.participants.exclude(id=instance.sender.id).first()
        
        if recipient:
            # Create the database notification
            notification = Notification.objects.create(
                user=recipient,
                type='message',
                title=f"New Message from {instance.sender.username}",
                content=instance.text[:50] + "..." if instance.text and len(instance.text) > 50 else instance.text or "Sent an attachment",
                link=f"/chat/chat/" # Or a specific conversation link
            )
            
            # Trigger real-time push via Channels
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f"user_{recipient.id}",
                    {
                        "type": "notification_message",
                        "data": {
                            "id": notification.id,
                            "type": "message",
                            "title": notification.title,
                            "content": notification.content,
                            "created_at": notification.created_at.strftime("%H:%M"),
                        }
                    }
                )
            
            # Send Web Push notification (for mobile/closed app notifications)
            try:
                from .utils import send_web_push
                send_web_push(
                    user=recipient,
                    title=notification.title,
                    message=notification.content,
                    link=notification.link
                )
            except Exception as e:
                print(f"Error triggering send_web_push: {e}")
