from django.views.generic import DetailView, ListView
from .models import Organization


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization
