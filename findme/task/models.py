from django.db import models
from django.conf import settings

def upload_image_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    return '%s%s' % (str(filename_base),filename_ext)

class Task(models.Model):
    question = models.CharField(max_length=200, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    video = models.FileField(upload_to=upload_image_to, blank=True ,null=True)
    graph = models.ImageField(upload_to="sentiment_graph", blank=True, null=True) 
    
    class Meta:
        verbose_name = '영상'

