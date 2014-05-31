from django.contrib import admin

from .models import (Organization, LaborType, Task, Location)

admin.site.register(Location)
admin.site.register(LaborType)
admin.site.register(Task)
admin.site.register(Organization)
