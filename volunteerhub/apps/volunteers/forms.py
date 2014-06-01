import floppyforms as forms
from django.forms import ModelForm


class ProfileForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()


class ProjectForm(forms.ModelForm):
    class Meta:
        exclude = ['organization', 'lead_volunteers']
