from django.db import models
from django.utils import timezone


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
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.role}: {self.content}"