from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^', include('volunteers.urls')),
)
