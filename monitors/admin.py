from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'scheduler', 'downloader', 'extractor', 'processor', 'create_time')

admin.site.register(Service, ServiceAdmin)