from django.db import models
from django.conf import settings


class Review(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=False)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=100, null=True)

  
    class Meta:
        verbose_name = '후기'
    def __str__(self):
        now = str(self.create_date)
        return self.client.username+' 님의 후기'+" "+now[:10]

