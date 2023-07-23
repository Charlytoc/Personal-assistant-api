from django.urls import path
from .views import StudyPlanView, SectionView, SectionListView, AllStudyPlanView, CreateDiscussionView, CommentCreateView

app_name = 'learning'

urlpatterns = [
    path('me/studyplan', StudyPlanView.as_view(), name='study_plan_view'),
    path('studyplan', AllStudyPlanView.as_view(), name='AllStudyPlanView'),
    path('studyplan/<str:study_plan_slug>', SectionListView.as_view(), name='section_list_view'),
    path('section/<int:section_id>', SectionView.as_view(), name='section_view'),
    path('discussion', CreateDiscussionView.as_view(), name='section_view'),
    path('comment', CommentCreateView.as_view(), name='section_view'),
]

