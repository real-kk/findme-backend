from django.db import models
from django.conf import settings


class Diary(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    sentiment_score = models.FloatField(verbose_name="텍스트감정분석결과", null=True)

    class Meta:
        verbose_name = '감정일기'
    
class DiaryWholeContent(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    whole_content = models.CharField(max_length=10000, null=True)
    image = models.ImageField(upload_to="wordcloud/", blank=True, null=True)

    class Meta:
        verbose_name = "감정일기 내용 모음"