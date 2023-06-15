from django.contrib import admin

# Register your models here.
from .models import Engine, Agent, Conversation, Message, TextDocument

@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'engine_provider', 'created_at')
    search_fields = ('name', 'slug')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'function_slug', 'engine', 'created_at')
    search_fields = ('name', 'function_slug')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user', 'token_count', 'started_at', 'ended_at', 'created_at')
    search_fields = ('title', 'user__username', 'agent__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'role', 'conversation', 'created_at')
    search_fields = ('content', 'role', 'conversation__title')

@admin.register(TextDocument)
class TextDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'organization', 'created_at')
    search_fields = ('title', 'slug', 'organization__name')