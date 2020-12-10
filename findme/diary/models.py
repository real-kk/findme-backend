from django.db import models
from django.conf import settings


class Diary(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    create_date = models.DateTimeField( null=True)
    content = models.CharField(max_length=1000)
    sentiment_score = models.FloatField(verbose_name="텍스트감정분석결과", null=True)

    class Meta:
        verbose_name = '감정일기'
    
class DiaryWholeContent(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    whole_content = models.CharField(max_length=10000, null=True)
    image = models.ImageField(upload_to="wordcloud/", blank=True, null=True)
    renew_flag = models.BooleanField(default=False)

    class Meta:
        verbose_name = "감정일기 내용 모음"

class LineGraph(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    line_graph = models.ImageField(upload_to="linegraph/", blank=True, null=True)

    class Meta:
        verbose_name = "꺾은선그래프 - 감정일기"
