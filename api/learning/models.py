from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

class Community(models.Model):
        name = models.CharField(max_length=255)
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
        description = models.TextField()
        is_public = models.BooleanField(default=True)
        invitation_token = models.UUIDField(default=uuid.uuid4, editable=False)
        tags = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
        TYPE_CHOICES = (
                ('HUMAN', 'Human'),
                ('AI', 'AI'),
        )
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        username = models.CharField(max_length=255)
        communities = models.ManyToManyField(Community, blank=True)
        is_public = models.BooleanField(default=True)
        biography = models.TextField(null=True, blank=True)
        profile_type = models.CharField(max_length=25, choices=TYPE_CHOICES)
        character = models.TextField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

class StudyPlan(models.Model):
        created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
        title = models.CharField(max_length=255)
        slug = models.CharField(max_length=255, null=True, blank=True)
        suggested_title = models.CharField(max_length=255, null=True, blank=True)
        description = models.TextField()
        number_of_sections = models.IntegerField(default=5)
        total_spent = models.DecimalField(decimal_places=5, default=0.00, max_digits=5)
        ai_description = models.TextField(null=True, blank=True)
        communities = models.ManyToManyField(Community,blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        def save(self, *args, **kwargs):
                
                # Generate slug based on name
                self.slug = slugify(self.title)
                super().save(*args, **kwargs)
class Section(models.Model):
        title = models.CharField(max_length=255)
        slug = models.CharField(max_length=255, null=True, blank=True)
        objective = models.TextField()
        study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
        created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        def save(self, *args, **kwargs):
                # Generate slug based on name
                self.slug = slugify(self.title)
                super().save(*args, **kwargs)
                
class Topic(models.Model):
        title = models.CharField(max_length=255)
        explanation = models.TextField(default='')
        section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
        
        objective = models.TextField(null=True, blank=True)
        created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

class Discussion(models.Model):
        created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
        topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
        text = models.TextField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
        profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
        discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
        text = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)