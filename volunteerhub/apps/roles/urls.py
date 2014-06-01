from django.conf.urls import patterns, url
from .views import DashboardView

# custom views
urlpatterns = patterns(
    '',
    url(r'dashboard/',
        view=DashboardView.as_view(),
        name="dashboard"),
)
