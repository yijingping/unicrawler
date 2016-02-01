from django.contrib import admin
from .models import Seed, IndexRule, DetailRule


class SeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'weight', 'status')
    list_filter = ['status']

admin.site.register(Seed, SeedAdmin)


class IndexRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'seed', 'name', 'site', 'url', 'frequency', 'update_time', 'next_crawl_time', 'fresh_pages', 'status')
    list_filter = ['status', 'update_time', 'next_crawl_time']

admin.site.register(IndexRule, IndexRuleAdmin)


class DetailRuleAdmin(admin.ModelAdmin):
    list_display = ['index_rule']

admin.site.register(DetailRule, DetailRuleAdmin)
