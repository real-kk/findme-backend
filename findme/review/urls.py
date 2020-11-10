from . import views
from django.urls import path


urlpatterns = [
    path('', views.Review_upload.as_view(), name='review_upload'),
]