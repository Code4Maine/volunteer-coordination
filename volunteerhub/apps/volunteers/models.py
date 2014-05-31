from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import (TitleSlugDescriptionModel,
                                         TimeStampedModel)
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from taggit.managers import TaggableManager
from .utils import get_lat_long
from django.auth.user.models import User


class Location(TimeStampedModel):
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


class Organization(TimeStampedModel, TitleSlugDescriptionModel):
    phone = PhoneNumberField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return ('organization-detail', None, {'slug': self.slug})

    def __unicode__(self):
        return u'{0}'.format(self.title)


class LaborType(TitleSlugDescriptionModel):
    pass

    @permalink
    def get_absolute_url(self):
        return ('task-type', None, {'slug': self.slug})

    def __unicode__(self):
        return u'{0}'.format(self.title)


class Project(TimeStampedModel, TitleSlugDescriptionModel):
    lead_volunteer = models.ForeignKey(User)
    image = models.ImageField()

    @permalink
    def get_absolute_url(self):
        return ('project-detail', None, {'slug': self.slug})

    def __unicode__(self):
        return u'{0}'.format(self.title)


class Task(TimeStampedModel, TitleSlugDescriptionModel):
    project = models.ForeignKey(Project)
    location = models.ForeignKey(Location, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    organization = models.ForeignKey(Organization, related_name='organization')
    labor_type = models.ForeignKey(LaborType, blank=True, null=True)

    requirements = TaggableManager()

    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return (
            'artifact-detail',
            None,
            {'organization-slug': self.organization.slug, 'slug': self.slug})

    def __unicode__(self):
        return u'{0} for {1}'.format(self.title, self.organization)

    @property
    def location(self):
        if len(self.locations.all()) == 1:
            return self.locations.all()[0]
        else:
            return False

