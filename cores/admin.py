from django.contrib import admin
from .models import Schema, Seed, Rule


class SchemaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Schema, SchemaAdmin)


class SeedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Seed, SeedAdmin)


class RuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Rule, RuleAdmin)
