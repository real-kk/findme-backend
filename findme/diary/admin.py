from django.contrib import admin

from diary import models

admin.site.register(models.Diary)
admin.site.register(models.DiaryWholeContent)
admin.site.register(models.LineGraph)