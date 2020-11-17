from django.db import models
from django.conf import settings
def upload_image_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    return '%s%s' % (filename_base,filename_ext )

class Task(models.Model):
    question = models.CharField(max_length=200, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    video= models.FileField(upload_to=upload_image_to, blank=True ,null=True)
    class Meta:
        verbose_name = '영상'

    def __str__(self):
        now = str(self.create_date)
        return self.client.username+'비디오'+" "+now[:10]
