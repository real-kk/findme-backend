from django.db import models


class Voice(models.Model):
    voice = models.FileField(upload_to="voice/", blank=True ,null=True)
    text = models.CharField(max_length=10000, null=True)
