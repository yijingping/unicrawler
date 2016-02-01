from django.contrib import admin
from .models import Site, Proxy


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain', 'proxy', 'browser', 'limit_speed', 'status')
    list_filter = ['proxy', 'browser', 'status']

admin.site.register(Site, SiteAdmin)


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'speed', 'status', 'retry', 'address')
    list_filter = ('status',)

admin.site.register(Proxy, ProxyAdmin)