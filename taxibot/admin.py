from django.contrib import admin

from taxibot.models import *



class CarInline(admin.TabularInline):
    model = Car


class TaxiCallAdmin(admin.ModelAdmin):
    fieldsets = [
                 ("data", {"fields": ["address", "type", "number","details","longitude","latitude","IsMap","status"], 'classes': ['collapse']}),
                 ]
    inlines = [CarInline]

admin.site.register(TaxiCall,TaxiCallAdmin)
