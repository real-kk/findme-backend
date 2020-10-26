from . import views
from django.urls import path


urlpatterns = [
    path('videos', views.Task.as_view(), name='task')
]