from . import views
from django.urls import path


urlpatterns = [
    path('', views.Review_upload.as_view(), name='review_upload'),
    path('counselors/', views.Review_get_by_counselor.as_view(), name='Review_get_by_counselor'),
    path('clients/', views.Review_get_by_client.as_view(), name='Review_get_by_client'),
]