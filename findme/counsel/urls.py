from . import views
from django.urls import path


urlpatterns = [
    path('', views.Counsel_application.as_view(), name='counsel_application'),
    path('<int:id>/', views.Counsel_application.as_view(), name='delete_counsel_application'),
    path('date/', views.CounselDate.as_view(), name='update_counsel_for_date'),
    path('photo/<int:id>/', views.CounselPhoto.as_view(), name="update_counsel_photo")

]
