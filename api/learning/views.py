from django.shortcuts import render
from .models import StudyPlan
from .serializers import SmallStudyPlanSerializer
# Create your views here.
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import StudyPlan, Section
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from api.aitools.actions import get_user_from_token
import json


@method_decorator(csrf_exempt, name='dispatch')
class StudyPlanView(View):
    def get(self, request, *args, **kwargs):
        # get the token from the request authorization header
        # it will be like: Authorization: Token {token_key}
        
        token_key = request.headers.get('Authorization').split()[1]
        user = get_user_from_token(token_key)

        study_plans = StudyPlan.objects.filter(created_by__user=user)

        study_plan_data = SmallStudyPlanSerializer(study_plans, many=True).data
     
        return JsonResponse(study_plan_data, safe=False)
    
    def post(self, request, *args, **kwargs):
            data = json.loads(request.body)
            study_plan = StudyPlan.objects.create(**data)
            return JsonResponse({'study_plan_id': study_plan.id})
    def put(self, request, *args, **kwargs):
            data = json.loads(request.body)
            StudyPlan.objects.filter(pk=kwargs['pk']).update(**data)
            return JsonResponse({'message': 'StudyPlan updated successfully'})
    
@method_decorator(csrf_exempt, name='dispatch')
class SectionView(View):
    def get(self, request, *args, **kwargs):
            section = get_object_or_404(Section, pk=kwargs['pk'])
            data = serializers.serialize('json', [section,])
            return JsonResponse(data, safe=False)
    def post(self, request, *args, **kwargs):
            data = json.loads(request.body)
            section = Section.objects.create(**data)
            return JsonResponse({'section_id': section.id})
    def put(self, request, *args, **kwargs):
            data = json.loads(request.body)
            Section.objects.filter(pk=kwargs['pk']).update(**data)
            return JsonResponse({'message': 'Section updated successfully'})