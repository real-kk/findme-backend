from . import views
from django.urls import path


urlpatterns = [
        path('videos/<int:id>/', views.TaskUpload.as_view(), name='taskUpload'),
    path('', views.TaskDetail.as_view(), name='TaskDetail'),
    path('questions/', views.AddTaskQuestion.as_view(), name='TaskQuestion'),
    path('process_videos/<int:id>/', views.VideoProcessing.as_view(), name='VideoProcessing'),
    path('questions_counselor/', views.TaskQuestionForCounselor.as_view(), name="QuestionForCounselor"),
]
