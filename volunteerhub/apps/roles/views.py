from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import Volunteer
from .forms import ProfileForm


class DashboardView(DetailView):
    ''' DashboardView

    
    '''
    model = Volunteer
    template_name = 'roles/dashboard.html'

    def get_object(self, *args, **kwargs):
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = Volunteer
    template_name = 'roles/profile_update.html'
    form_class = ProfileForm

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs()['initial'])

