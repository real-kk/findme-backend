from django.contrib import admin

from task import models

admin.site.register(models.Task)
admin.site.register(models.SentimentGraph)
