from django.urls import path

from . import views

urlpatterns = [
    path('', views.chat_page, name='chat-page'),
    path('conversations/', views.conversations_list, name='chat-conversations'),
    path('conversations/create/', views.conversation_create, name='chat-conversation-create'),
    path('messages/', views.chat_messages, name='chat-messages'),
    path('send/', views.chat_send, name='chat-send'),
    path('read/', views.chat_read, name='chat-read'),
    path('delete/', views.message_delete, name='chat-delete'),
    path('typing/', views.chat_typing, name='chat-typing'),
    path('unread/', views.chat_unread, name='chat-unread'),
    path('users/', views.users_page, name='chat-users-page'),
    path('users/data/', views.users_data, name='chat-users-data'),
    path('users/history/', views.users_history_page, name='chat-users-history-page'),
    path('users/history/data/', views.users_history_data, name='chat-users-history-data'),
]
