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
