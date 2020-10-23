from . import views
from django.urls import path


urlpatterns = [
    path('diaries/', views.Text_extract_wordcloud.as_view(), name='text_extract_wordcloud')
]