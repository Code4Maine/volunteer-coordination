from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import (TitleSlugDescriptionModel,
                                         TimeStampedModel)
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from .utils import get_lat_long
from django.contrib.auth import get_user_model


class Location(TimeStampedModel):
    '''
    Location model.

    '''
    slug = models.SlugField(_('slug'))
    address = models.CharField(_('address'),
                               max_length=255, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    state = USStateField(_('state'), blank=True, null=True)
    zipcode = models.CharField(_('zip'), max_length=5, blank=True, null=True)
    lat_long = models.CharField(_('lat and long coords'),
                                max_length=255, blank=True, null=True)
    point = gis_models.PointField(blank=True, null=True)

    def __unicode__(self):
        return u'{0}, {1}, {2}'.format(self.address, self.city, self.state)

    @property
    def latitude(self):
        return float(self.lat_long.split(',')[0])

    @property
    def longitude(self):
        return float(self.lat_long.split(',')[1])

    @permalink
    def get_absolute_url(self):
        return ('location-detail', None, {'slug': self.slug})

    def save(self):
        location = "%s+%s+%s+%s" % (self.address.replace(' ', '+'),
                                    self.city,
                                    self.state,
                                    self.zipcode)
        self.lat_long = get_lat_long(location)
        if not self.lat_long:
            location = "%s+%s+%s" % (self.city, self.state, self.zipcode)
            self.lat_long = get_lat_long(location)
        self.point = GEOSGeometry(
            'POINT(%s)' % self.lat_long.replace(',', ' '))

        super(Location, self).save()


class Volunteer(TimeStampedModel):
    '''
    '''
    name = models.TextField(_('Name'), max_length=255)
    phone_number = PhoneNumberField(blank=True, null=True)

    opportunities_completed = models.ManyToManyField('projects.Opportunity')

    @property
    def is_manager(self):
        if self.organization_set.all():
            return True
        else:
            return False
