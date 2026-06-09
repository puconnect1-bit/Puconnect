import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversation, Message, Notification

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.conv_id = int(self.scope['url_route']['kwargs']['conv_id'])
            self.room_group_name = f'chat_{self.conv_id}'
            
            user = self.scope.get('user')
            if not user or not user.is_authenticated:
                print(f"Connection rejected: Unauthenticated user")
                await self.close()
                return

            print(f"User {user.username} connecting to {self.room_group_name}")

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            print(f"Connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user = self.scope.get('user')
            
            if not user or not user.is_authenticated:
                print("Unauthorized attempt to send message")
                return

            # Save message to database and get notifications data
            result = await self.save_message_and_create_notifications(
                user.id, 
                data.get('message'), 
                data.get('image_url'), 
                data.get('voice_url'),
                data.get('meetup_spot'),
                data.get('meetup_time')
            )
            
            saved_msg = result['message']
            notifications = result['notifications']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data.get('message'),
                    'image_url': data.get('image_url'),
                    'voice_url': data.get('voice_url'),
                    'meetup_spot': data.get('meetup_spot'),
                    'meetup_time': data.get('meetup_time'),
                    'sender_id': user.id,
                    'sender_username': user.username,
                    'timestamp': saved_msg.timestamp.strftime("%I:%M %p")
                }
            )

            # Send real-time notifications to each recipient
            print(f"DEBUG: Broadcasting notifications to {len(notifications)} recipients")
            for notif in notifications:
                print(f"DEBUG: Sending to user_{notif['user_id']}")
                await self.channel_layer.group_send(
                    f"user_{notif['user_id']}",
                    {
                        'type': 'notification_message',
                        'data': {
                            'id': notif['id'],
                            'title': notif['title'],
                            'content': notif['content'],
                            'created_at': 'Just now'
                        }
                    }
                )
        except Exception as e:
            print(f"Receive error: {e}")

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'image_url': event.get('image_url'),
            'voice_url': event.get('voice_url'),
            'meetup_spot': event.get('meetup_spot'),
            'meetup_time': event.get('meetup_time'),
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message_and_create_notifications(self, sender_id, text, image_url, voice_url, meetup_spot, meetup_time):
        user = User.objects.get(id=sender_id)
        conv = Conversation.objects.get(id=self.conv_id)
        # Update conversation timestamp so it moves to top of list
        conv.save() 
        
        msg = Message.objects.create(
            conversation=conv,
            sender=user,
            text=text,
            image_url=image_url,
            voice_url=voice_url,
            meetup_spot=meetup_spot,
            meetup_time=meetup_time
        )

        notifications_data = []
        content = text[:50] + "..." if text and len(text) > 50 else text or "Sent an attachment"
        
        for participant in conv.participants.exclude(id=sender_id):
            notif = Notification.objects.create(
                user=participant,
                type='message',
                title=f"New message from {user.username}",
                content=content,
                link=f"/chat/"
            )
            notifications_data.append({
                'id': notif.id,
                'user_id': participant.id,
                'title': notif.title,
                'content': notif.content
            })
            
        return {
            'message': msg,
            'notifications': notifications_data
        }
