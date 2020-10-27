from django.db import models
from django.conf import settings

class Task(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    title= models.CharField(max_length=200)
    video= models.FileField(upload_to="video/", blank=True ,null=True)
    class Meta:
        verbose_name = '영상과제'

    def __str__(self):
        return self.title