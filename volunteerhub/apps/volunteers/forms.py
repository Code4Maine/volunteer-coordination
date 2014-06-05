from django.core.urlresolvers import reverse
import floppyforms as forms
from .models import Volunteer, Project, Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization

    def get_success_url(self):
        return reverse('dashboard')


class VolunteerForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Volunteer
        exclude = ['opportunities_completed', 'user']

    def get_success_url(self):
        return reverse('dashboard')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['organization', 'lead_volunteers']
