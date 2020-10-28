from . import views
from django.urls import path


urlpatterns = [
    path('', views.Counsel_application.as_view(), name='counsel_application')
]