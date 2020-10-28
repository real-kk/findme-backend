from django.db import models
from django.conf import settings


class Counsel(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=False)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    major = models.CharField(max_length=100)
    student_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    time_table = models.ImageField(upload_to="image/", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = '신청서'
    
