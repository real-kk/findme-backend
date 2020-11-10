from django.db import models

class Review(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=False)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = '후기'
