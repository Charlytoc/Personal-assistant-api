from django.urls import path
from .views import follow_conversation
app_name = 'aitools'

urlpatterns = [
    path('conversation/<int:conversation_id>/message', follow_conversation, name='message'),
]

