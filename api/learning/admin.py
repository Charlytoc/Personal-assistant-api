
# Register your models here.
from django.contrib import admin
from .models import Community, Profile, StudyPlan, Section, Topic, Discussion, Comment
from .actions import create_topics_for_a_section, get_topic_content, create_sections_from_studyplan, create_studyplan_description_from_studyplan

class CommunityAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Community._meta.fields]
       
admin.site.register(Community, CommunityAdmin)
class ProfileAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Profile._meta.fields]
        filter_horizontal = ('communities',)
admin.site.register(Profile, ProfileAdmin)

class StudyPlanAdmin(admin.ModelAdmin):
        actions = ['create_sections_from_study_plan', 'create_studyplan_description']
        
        def create_sections_from_study_plan(self, request, queryset):
              for study_plan in queryset:
                    create_sections_from_studyplan(study_plan=study_plan)

        def create_studyplan_description(self, request, queryset):
              for study_plan in queryset:
                    create_studyplan_description_from_studyplan(study_plan=study_plan)

        list_display = [field.name for field in StudyPlan._meta.fields]
        filter_horizontal = ('communities',)
admin.site.register(StudyPlan, StudyPlanAdmin)

class SectionAdmin(admin.ModelAdmin):
    actions = ['get_topic_from_section']
    list_display = [field.name for field in Section._meta.fields]

    def get_topic_from_section(self, request, queryset):
        for section in queryset:
            create_topics_for_a_section(section)


admin.site.register(Section, SectionAdmin)

class TopicAdmin(admin.ModelAdmin):
    actions = ['generate_topic_content']

    def generate_topic_content(self, request, queryset):
        for topic in queryset:
            get_topic_content(topic=topic)

    list_display = [field.name for field in Topic._meta.fields]

admin.site.register(Topic, TopicAdmin)
class DiscussionAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Discussion._meta.fields]
admin.site.register(Discussion, DiscussionAdmin)
class CommentAdmin(admin.ModelAdmin):
        list_display = [field.name for field in Comment._meta.fields]
admin.site.register(Comment, CommentAdmin)