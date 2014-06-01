from django.conf.urls import patterns, url
from .views import (OrganizationDetailView, OrganizationListView)

# custom views
urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-\w]+)/',
        view=OrganizationDetailView.as_view(),
        name="organization-detail"),

    url(r'^$',
        view=OrganizationListView.as_view(),
        name="organization-list"),
)
