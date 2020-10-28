from . import views
from django.urls import path


urlpatterns = [
    path('diaries/', views.Text_extract_wordcloud.as_view(), name='text_extract_wordcloud'),
    path('whole_content/', views.Whole_content_to_wordcloud.as_view(), name="whole_content_to_wc")
]