from django.contrib import admin

from .models import (Organization, LaborType, Opportunity, Location,
                     Project, VolunteerApplication, Volunteer)


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("address", "city", "state",)}
    list_display = ('address', 'city', 'state')
    list_filter = ('city', 'state')

admin.site.register(Location, LocationAdmin)
admin.site.register(LaborType)
admin.site.register(Opportunity)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(VolunteerApplication)
admin.site.register(Volunteer)
