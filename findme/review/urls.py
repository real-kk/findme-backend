from . import views
from django.urls import path


urlpatterns = [
    path('', views.Review_upload.as_view(), name='review_upload'),
    path('counselors/<int:id>/', views.Review_get_by_counselor.as_view(), name='Review_get_by_counselor'),
    path('<int:id>/', views.Review_upload.as_view(), name='Review_upload'),
<<<<<<< HEAD
    path('clients/<int:id>/', views.Review_get_by_client.as_view(), name='Review_get_by_client'),
=======
    path('clients/', views.Review_get_by_client.as_view(), name='Review_get_by_client'),
>>>>>>> main
]