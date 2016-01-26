from django.contrib import admin
from .models import Seed, IndexRule, DetailRule


class SeedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Seed, SeedAdmin)


class IndexRuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(IndexRule, IndexRuleAdmin)


class DetailRuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(DetailRule, DetailRuleAdmin)
