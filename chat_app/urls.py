from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/messages/<int:conv_id>/', views.get_messages, name='get_messages'),
    path('api/start/', views.start_conversation, name='start_conversation'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/read-all/', views.mark_notifications_read, name='mark_notifications_read'),
]
