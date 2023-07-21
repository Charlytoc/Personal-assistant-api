from django.shortcuts import render, get_object_or_404
from .models import StudyPlan
from .serializers import SmallStudyPlanSerializer, SmallSectionSerializer,BigStudyPlanSerializer
from django.views.generic import ListView

from .models import StudyPlan, Section
from django.views import View
from django.http import JsonResponse
from .models import StudyPlan, Section
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from api.aitools.actions import get_user_from_token
import json
from .actions import separate_text, get_user_profile, get_better_studyplan_description, create_sections_from_studyplan, create_topics_for_all_studyplan_sections

from structlog import get_logger

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
        # logger = logger.bind(request=request)
        logger.info('Received POST request')

        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)
        profile = get_user_profile(user)
        data = json.loads(request.body)
        title = data.get('title', '')
        description = data.get('description', '')
        create_sections = data.get('create_sections', False)

        study_plan = StudyPlan(
              created_by = profile,
              title=title,
              description=description
        )
        ai_description = get_better_studyplan_description(description)
        title, description = separate_text(ai_description, '_tit_')
        study_plan.ai_description = description
        study_plan.suggested_title = title
        study_plan.save()
        if create_sections:
                create_sections_from_studyplan(
                study_plan=study_plan
                )
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
    def get(self, request, *args, **kwargs):
        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)
        profile = get_user_profile(user)
        
        studyplan_id = request.GET.get('studyplan')
        if studyplan_id:
            sections = Section.objects.filter(study_plan__id=studyplan_id)
        else:
            sections = Section.objects.filter(study_plan__created_by=profile)
        
        serializer_data = SmallSectionSerializer(sections, many=True).data
        return JsonResponse(serializer_data, safe=False)
    

#     def post(self, request, *args, **kwargs):
#             data = json.loads(request.body)
#             section = Section.objects.create(**data)
#             return JsonResponse({'section_id': section.id})
#     def put(self, request, *args, **kwargs):
#             data = json.loads(request.body)
#             Section.objects.filter(pk=kwargs['pk']).update(**data)
#             return JsonResponse({'message': 'Section updated successfully'})
    


class SectionListView(View):
    def get(self, request, study_plan_slug):
        study_plan = get_object_or_404(StudyPlan, slug=study_plan_slug)
        # sections = study_plan.section_set.all()
        serializer_data = BigStudyPlanSerializer(study_plan).data
        return JsonResponse(serializer_data, safe=False)
    
