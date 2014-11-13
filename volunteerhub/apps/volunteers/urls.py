from django.conf.urls import patterns, url
from .views import (OpportunityDetailView, ProjectListView,
                    ProjectDetailView, ProjectListJSONView,
                    ProjectDetailJSONView, OpportunityDetailJSONView,
                    DashboardView, ProfileUpdateView, ProjectCreateView,
                    OpportunityVolunteerView, OpportunityUnVolunteerView,
                    OrganizationCreateView)
import volunteers.views as views

# custom views
urlpatterns = patterns(
    '',
    url(r'^projects/add/$',
        view=views.ProjectCreateView.as_view(),
        name="project-create"),

    url(r'^projects/(?P<slug>[-\w]+)/opportunities/add/$',
        view=views.OpportunityCreateView.as_view(),
        name="opportunity-create"),

    url(r'^projects/(?P<slug>[-\w]+)/opportunities.json$',
        view=views.ProjectDetailJSONView.as_view(),
        name="project-detail-json"),

    url(r'^projects/(?P<project_slug>[-\w]+)/(?P<slug>[-\w]+)/unvolunteer/$',
        view=views.OpportunityUnVolunteerView.as_view(),
        name="opportunity-unvolunteer"),

    url(r'^projects/(?P<project_slug>[-\w]+)/(?P<slug>[-\w]+)/volunteer/$',
        view=views.OpportunityVolunteerView.as_view(),
        name="opportunity-volunteer"),

    url(r'^projects/(?P<project_slug>[-\w]+)/(?P<slug>[-\w]+).json$',
        view=views.OpportunityDetailJSONView.as_view(),
        name="opportunity-detail-json"),

    url(r'^projects/(?P<project_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        view=views.OpportunityDetailView.as_view(),
        name="opportunity-detail"),

    url(r'^projects/(?P<slug>[-\w]+)/$',
        view=views.ProjectDetailView.as_view(),
        name="project-detail"),

    url(r'^organization/add/$',
        view=views.OrganizationCreateView.as_view(),
        name="organization-create"),

    url(r'^projects.json$',
        view=views.ProjectListJSONView.as_view(),
        name="project-list-json"),

    url(r'^projects/$',
        view=views.ProjectListView.as_view(),
        name="project-list"),

    url(r'dashboard/edit-profile/$',
        view=views.ProfileUpdateView.as_view(),
        name="profile-update"),

    url(r'dashboard/$',
        view=views.DashboardView.as_view(),
        name="dashboard"),

    url(r'change-organization/$',
        view=views.change_organization,
        name="change-organization"),

    url(r'^$',
        view=views.ProjectListView.as_view(),
        name="homepage"),

)
