from django.urls import path
from .views import StudyPlanView, SectionView, SectionListView

app_name = 'learning'

urlpatterns = [
    path('studyplan', StudyPlanView.as_view(), name='study_plan_view'),
    path('studyplan/<int:study_plan_id>/sections', SectionListView.as_view(), name='section_list_view'),
    path('section', SectionView.as_view(), name='section_view'),
]

