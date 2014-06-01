import floppyforms as forms


class ProfileForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
