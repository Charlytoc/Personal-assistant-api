from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from ..authenticate.models import EngineProvider, Organization
from django.utils.text import slugify
import base64



class Engine(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(help_text="This must be an identificator for the provider")
    description = models.TextField(blank=True, null=True)
    engine_provider = models.ForeignKey(EngineProvider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Agent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    function_slug = models.SlugField(help_text="This is an internal identificator for the function to be executed when this agent runs")
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    token_count = models.IntegerField(blank=True, null=True)

    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    USER = 'USER'
    SYSTEM = 'SYSTEM'
    ASSISTANT = 'ASSISTANT'

    ROLE_CHOICES = [
        (USER, 'User'),
        (SYSTEM, 'System'),
        (ASSISTANT, 'Assistant'),
    ]

    content = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.role}: {self.content}"
    
class TextDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Encode content as base64 to protect personal data
        self.content = base64.b64encode(self.content.encode()).decode()
        # Generate slug based on name
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name