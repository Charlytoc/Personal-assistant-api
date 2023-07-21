from django.urls import path
from .views import StudyPlanView, SectionView, SectionListView, AllStudyPlanView

app_name = 'learning'

urlpatterns = [
    path('me/studyplan', StudyPlanView.as_view(), name='study_plan_view'),
    path('studyplan', AllStudyPlanView.as_view(), name='AllStudyPlanView'),
    path('studyplan/<str:study_plan_slug>', SectionListView.as_view(), name='section_list_view'),
    path('section', SectionView.as_view(), name='section_view'),
]

