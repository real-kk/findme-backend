from django.urls import path, include
from voice import views

urlpatterns = [
    path('', views.VoiceSTT.as_view(), name='VoiceSTT'),
]
