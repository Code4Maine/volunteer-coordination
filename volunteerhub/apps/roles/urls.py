from django.conf.urls import patterns, url
from .views import DashboardView, ProfileUpdateView

# custom views
urlpatterns = patterns(
    '',
    url(r'dashboard/edit-profile/',
        view=ProfileUpdateView.as_view(),
        name="profile-update"),

    url(r'dashboard/',
        view=DashboardView.as_view(),
        name="dashboard"),
)
