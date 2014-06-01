from django.views.generic import DetailView, ListView, TemplateView
from .models import Organization


class DashboardView(TemplateView):
    ''' DashboardView

    
    '''
    template_name = 'roles/dashboard.html'


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization
