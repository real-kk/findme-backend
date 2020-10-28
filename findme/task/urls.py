from . import views
from django.urls import path


urlpatterns = [
    path('videos', views.TaskUpload.as_view(), name='taskUpload')
]