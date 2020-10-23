from django.db import models


class Diary(models.Model):

    title = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=1000)

    class Meta:
        verbose_name = '감정일기'
    
