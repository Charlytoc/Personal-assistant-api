
from django.utils import timezone
from datetime import timedelta
import string
import secrets

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import datetime

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

class OrganizationMember(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

class EngineProvider(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class ProviderCredentials(models.Model):
    key = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    engine_provider = models.ForeignKey(EngineProvider, on_delete=models.CASCADE)
    expiration_date = models.DateField(default=datetime.date.today() + timedelta(days=60))

    created_at = models.DateTimeField(auto_now_add=True)



class Token(models.Model):

    key = models.CharField(max_length=255, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))

    def save(self, *args, **kwargs):
        self.key = Token.generate_unique_token()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_token(length=20):
        characters = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(characters) for _ in range(length))
        return token
    

class TokenUsage(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
