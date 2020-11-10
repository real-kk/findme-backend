from . import views
from django.urls import path


urlpatterns = [
    path('/', views.Review.as_view(), name='review'),
]