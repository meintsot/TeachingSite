from django.contrib import admin
from . import models

admin.site.register(models.Announcement)
admin.site.register(models.Category)
admin.site.register(models.Lesson)
admin.site.register(models.HomeWork)
admin.site.register(models.Token)