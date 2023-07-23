import json
from structlog import get_logger

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views import View

from api.aitools.actions import get_user_from_token

from .actions import (separate_text, create_topics_for_a_section, get_user_profile, get_better_studyplan_description,
                      create_sections_from_studyplan, create_topics_for_all_studyplan_sections, create_studyplan_description_from_studyplan,
                      comment_with_ai_from_topic_and_discussion, create_comment)
from .models import Discussion, Profile, Section, StudyPlan, Topic, Comment
from .serializers import (BigSectionSerializer, BigStudyPlanSerializer, SmallSectionSerializer, SmallStudyPlanSerializer,DiscussionSerializer)

logger = get_logger()


@method_decorator(csrf_exempt, name='dispatch')
class StudyPlanView(View):
    def get(self, request, *args, **kwargs):
        '''
        This view its already trusted
        '''
        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)
        study_plans = StudyPlan.objects.filter(created_by__user=user)
        study_plan_data = SmallStudyPlanSerializer(study_plans, many=True).data
        return JsonResponse(study_plan_data, safe=False)
    
    def post(self, request, *args, **kwargs):
        '''
        This view its already trusted
        '''
        logger.info('Received POST request')

        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)
        profile = get_user_profile(user)

        data = json.loads(request.body)
        title = data.get('title', '')
        description = data.get('description', '')

        study_plan = StudyPlan(
              created_by = profile,
              title=title,
              description=description
        )
        create_studyplan_description_from_studyplan(study_plan)

        # if create_sections:
        #         create_sections_from_studyplan(
        #         study_plan=study_plan
        #         )

        return JsonResponse({'study_plan_id': study_plan.id})
        
@method_decorator(csrf_exempt, name='dispatch')
class AllStudyPlanView(View):
    def get(self, request, *args, **kwargs):
        '''
        This view its already trusted
        '''
        study_plans = StudyPlan.objects.all()
        study_plan_data = BigStudyPlanSerializer(study_plans, many=True).data
        return JsonResponse(study_plan_data, safe=False)
    

@method_decorator(csrf_exempt, name='dispatch')
class SectionView(View):
    def get(self, request, section_id):
        # token_key = request.headers.get('Authorization').split()[1]
        # user = get_user_from_token(token_key)
        # profile = get_user_profile(user)
        section = Section.objects.get(pk=section_id)
        serializer_data = BigSectionSerializer(section).data
        print(serializer_data)
        return JsonResponse(serializer_data, safe=False)
    
    def post(self, request, section_id):
        # token_key = request.headers.get('Authorization').split()[1]
        # user = get_user_from_token(token_key)
        # profile = get_user_profile(user)
        section = Section.objects.get(pk=section_id)
        create_topics_for_a_section(section)
        serializer_data = BigSectionSerializer(section).data
        # print(serializer_data)
        return JsonResponse(serializer_data, safe=False)
    

@method_decorator(csrf_exempt, name='dispatch')
class SectionListView(View):
    def get(self, request, study_plan_slug):
        study_plan = get_object_or_404(StudyPlan, slug=study_plan_slug)
        # sections = study_plan.section_set.all()
        serializer_data = BigStudyPlanSerializer(study_plan).data
        return JsonResponse(serializer_data, safe=False)
    def post(self, request, study_plan_slug):
        study_plan = get_object_or_404(StudyPlan, slug=study_plan_slug)
        create_sections_from_studyplan(study_plan)
        serializer_data = BigStudyPlanSerializer(study_plan).data
        return JsonResponse(serializer_data, safe=False)
    
from .serializers import ProfileSerializer
from .models import Profile


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        profile = Profile.objects.create(**data)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)
    

@method_decorator(csrf_exempt, name='dispatch')  # Only if you want to exempt from CSRF protection
class CreateDiscussionView(View):
    def post(self, request, *args, **kwargs):
        try:
            token_key = request.headers.get('Authorization').split()[1]
            print(token_key)
            user = get_user_from_token(token_key)
            created_by = get_user_profile(user)

            # Parse the JSON data from the request
            data = json.loads(request.body)
            topic_id = data['topic_id']
            text = data['text']
            # Check if the topic exists
          
            topic = Topic.objects.get(id=topic_id)
            
            # # Create the new Discussion
            discussion = Discussion.objects.create(created_by=created_by, topic=topic, text=text)
            discussion.save()
          
            data= DiscussionSerializer(discussion).data
            return JsonResponse(data, status=201)
        
        except KeyError:
            return HttpResponseBadRequest("Invalid data! 'topicId' and 'text' are required.")
        except ValueError:
            return HttpResponseBadRequest("Invalid JSON format.")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Topic does not exist.")
        


@method_decorator(csrf_exempt, name='dispatch') 
class CommentCreateView(View):

    def post(self, request, *args, **kwargs):
        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)
        profile = get_user_profile(user)
        
        data = json.loads(request.body)
        discussion_id = data.get('discussion_id')
        with_ai = data.get('with_ai', False)
        comment = data.get('comment', None)
        
        # Get the discussion object
        discussion = get_object_or_404(Discussion, id=discussion_id)
        
        if with_ai and not comment:
            ai_comment = comment_with_ai_from_topic_and_discussion(discussion=discussion)

        comment = Comment.objects.create(
            profile=profile,
            discussion=discussion,
            text=ai_comment,
        )
        data= DiscussionSerializer(discussion).data
        return JsonResponse(data, status=201)