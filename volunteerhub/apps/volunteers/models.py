from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import TimeStampedField
from django.contrib.auth import get_user_model


class Volunteer(TimeStampedField):
    pass

