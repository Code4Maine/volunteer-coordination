from django.conf.urls import patterns, url
from .views import (OrganizationDetailView, OrganizationListView,
                    TaskDetailView, TaskListView)

# custom views
urlpatterns = patterns(
    '',
    url(r'^(?P<organization_slug>[-\w]+)/tasks/(?P<slug>[-\w]+)/',
        view=TaskDetailView.as_view(),
        name="task-detail"),

    url(r'^(?P<organization_slug>[-\w]+)/tasks/',
        view=TaskListView.as_view(),
        name="task-list"),

    url(r'^(?P<slug>[-\w]+)/',
        view=OrganizationDetailView.as_view(),
        name="organization-detail"),

    url(r'^$',
        view=OrganizationListView.as_view(),
        name="organization-list"),
)
