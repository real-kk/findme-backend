from . import views
from django.urls import path


urlpatterns = [
    path('', views.Counsel_application.as_view(), name='counsel_application'),
    path('date/', views.CounselDate.as_view(), name='update_counsel_for_date')
]