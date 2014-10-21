from django.conf.urls import patterns, url
from .views import (OpportunityDetailView, ProjectListView,
                    ProjectDetailView, DashboardView, ProfileUpdateView, 
                    ProjectCreateView,
                    OpportunityVolunteerView, OpportunityUnVolunteerView,
                    OrganizationCreateView)

# custom views
urlpatterns = patterns(
    '',
    url(r'^(?P<org_id>[\d]+)/projects/(?P<slug>[-\w]+)/opportunities/$',
        view=ProjectDetailView.as_view(),
        name="project-detail"),

    url(r'^(?P<org_id>[\d]+)/projects/add/(?P<slug>[-\w]+)/$',
        view=ProjectCreateView.as_view(),
        name="project-create"),

    url(r'^(?P<org_id>[\d]+)/projects/$',
        view=ProjectListView.as_view(),
        name="project-list"),

    url(r'^(?P<org_id>[\d]+)/dashboard/edit-profile/$',
        view=ProfileUpdateView.as_view(),
        name="profile-update"),

    url(r'^(?P<org_id>[\d]+)/dashboard/$',
        view=DashboardView.as_view(),
        name="dashboard"),

)

