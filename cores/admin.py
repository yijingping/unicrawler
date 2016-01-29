from django.contrib import admin
from .models import Seed, Site, IndexRule, DetailRule, Proxy


class SeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'weight', 'status')
    list_filter = ['status']

admin.site.register(Seed, SeedAdmin)


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain', 'proxy', 'browser', 'limit_speed', 'status')
    list_filter = ['proxy', 'browser', 'status']

admin.site.register(Site, SiteAdmin)


class IndexRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'seed', 'name', 'site', 'url', 'frequency', 'update_time', 'next_crawl_time', 'fresh_pages', 'status')
    list_filter = ['status', 'update_time', 'next_crawl_time']

admin.site.register(IndexRule, IndexRuleAdmin)


class DetailRuleAdmin(admin.ModelAdmin):
    list_display = ['index_rule']

admin.site.register(DetailRule, DetailRuleAdmin)


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'speed', 'status', 'retry', 'address')
    list_filter = ('status',)

admin.site.register(Proxy, ProxyAdmin)