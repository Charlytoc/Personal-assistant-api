from django.urls import path
from .views import follow_conversation, update_text_document
app_name = 'aitools'

urlpatterns = [
    path('conversation/<int:conversation_id>/message', follow_conversation, name='message'),
    path('document/<int:document_id>', update_text_document, name='message'),
]

