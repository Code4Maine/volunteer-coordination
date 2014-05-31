from django.contrib import admin

from .models import (Artifact, Organization, Tour, ArtifactType, TourStop,
                     Location)


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(ArtifactType, SlugAdmin)
admin.site.register(Organization, SlugAdmin)


class TourStopInline(admin.TabularInline):
    model = TourStop


class TourAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        TourStopInline,
    ]

admin.site.register(Tour, TourAdmin)


class ArtifactAdmin(SlugAdmin):
    pass

admin.site.register(Artifact, ArtifactAdmin)


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("address", "city", "state",)}
    list_display = ('address', 'city', 'state')
    list_filter = ('city', 'state')

admin.site.register(Location, LocationAdmin)
