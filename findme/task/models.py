from django.db import models
from django.conf import settings

def upload_image_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    return '%s%s' % (filename_base,filename_ext)

class Task(models.Model):
    question = models.CharField(max_length=200, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    video= models.FileField(upload_to=upload_image_to, blank=True ,null=True)
    anger = models.FloatField(verbose_name="화남", null=True, blank=True)
    contempt = models.FloatField(verbose_name="경멸", null=True, blank=True)
    disgust = models.FloatField(verbose_name="역겨움", null=True, blank=True)
    fear = models.FloatField(verbose_name="두려움", null=True, blank=True)
    happiness = models.FloatField(verbose_name="행복", null=True, blank=True)
    neutral = models.FloatField(verbose_name="중립", null=True, blank=True)
    sadness = models.FloatField(verbose_name="슬픔", null=True, blank=True)
    surprise = models.FloatField(verbose_name="놀람", null=True, blank=True)

    class Meta:
        verbose_name = '영상'

    def __str__(self):
        now = str(self.create_date)
        return self.client.username+'비디오'+" "+now[:10]

    def save(self, *args, **kwargs):
        from datetime import datetime
        self.video.name = datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".mp4"
        super(Task, self).save(*args, **kwargs)

class SentimentGraph(models.Model):
    image = models.ImageField(upload_to="sentiment_graph/", blank=True, null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "꺾은선그래프 - 영상감정"

        
