from django.contrib import admin

from .models import (Organization, LaborType, Task, Location)

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("address", "city", "state",)}
    list_display = ('address', 'city', 'state')
    list_filter = ('city', 'state')

admin.site.register(Location, LocationAdmin)
admin.site.register(LaborType)
admin.site.register(Task)
admin.site.register(Organization)
