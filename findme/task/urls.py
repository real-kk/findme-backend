from . import views
from django.urls import path


urlpatterns = [
    path('videos/', views.TaskUpload.as_view(), name='taskUpload'),
    path('', views.TaskDetail.as_view(), name='TaskDetail')
]