
# Register your models here.
from django.contrib import admin
from .models import Community, Profile, StudyPlan, Section, Topic, Discussion, Comment


class CommunityAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Community._meta.fields]
       
admin.site.register(Community, CommunityAdmin)
class ProfileAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Profile._meta.fields]
        filter_horizontal = ('communities',)
admin.site.register(Profile, ProfileAdmin)
class StudyPlanAdmin(admin.ModelAdmin):
        list_display = [field.name for field in StudyPlan._meta.fields]
        filter_horizontal = ('communities',)
admin.site.register(StudyPlan, StudyPlanAdmin)
class SectionAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Section._meta.fields]
admin.site.register(Section, SectionAdmin)
class TopicAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Topic._meta.fields]
admin.site.register(Topic, TopicAdmin)
class DiscussionAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Discussion._meta.fields]
admin.site.register(Discussion, DiscussionAdmin)
class CommentAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Comment._meta.fields]
admin.site.register(Comment, CommentAdmin)