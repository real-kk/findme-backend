from django.db import models
from django.conf import settings
def upload_image_to(instance, filename):
    import os
    filename_base, filename_ext = os.path.splitext(filename)
    return 'image/timetable/%s%s' % (filename_base,filename_ext )



class Counsel(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=False)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    major = models.CharField(max_length=100)
    student_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    time_table = models.ImageField(upload_to=upload_image_to, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_date.editable=True
    class Meta:
        verbose_name = '신청서'
    
    def __str__(self):
        now = str(self.create_date)
        return self.client.username+'신청서'+" "+now[:10]
