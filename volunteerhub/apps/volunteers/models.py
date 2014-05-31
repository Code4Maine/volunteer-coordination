from django.conf import settings
from datetime import datetime
from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from .utils import get_lat_long


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.

    Subclass new models from 'StandardMetadata' instead of 'models.Model'.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(default=datetime.now, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.title)


class Location(models.Model):
    address = models.CharField(_('address'),
                               max_length=255, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    state = USStateField(_('state'), blank=True, null=True)
    zipcode = models.CharField(_('zip'), max_length=5, blank=True, null=True)
    lat_long = models.CharField(_('lat and long coords'),
                                max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
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


class Organization(StandardMetadata, Location):
    phone = PhoneNumberField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return ('organization_detail', None, {'slug': self.slug})


class ArtifactType(StandardMetadata):
    slug = models.SlugField(unique=True)

    @permalink
    def get_absolute_url(self):
        return ('artifact_type_detail', None, {'slug': self.slug})


class Artifact(StandardMetadata):
    slug = models.SlugField(unique=True)
    organization = models.ForeignKey(Organization, related_name='organization')
    inventory_id = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=255, upload_to='artifacts')
    built = models.CharField(max_length=6, blank=True, null=True)
    architect = models.CharField(max_length=255, blank=True, null=True)
    style = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(ArtifactType)
    locations = models.ManyToManyField(Location, blank=True, null=True)

    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return (
            'artifact_detail',
            None,
            {'organization_slug': self.organization.slug, 'slug': self.slug})

    @property
    def location(self):
        if len(self.locations.all()) == 1:
            return self.locations.all()[0]
        else:
            return False


class TourLocation(StandardMetadata):
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=5)


class Tour(StandardMetadata):
    slug = models.SlugField(unique=True)
    image = models.ImageField(max_length=255, upload_to='tours')
    organization = models.ForeignKey(Organization)
    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return (
            'tour_detail',
            None,
            {'organization_slug': self.organization.slug, 'slug': self.slug})


class TourStop(StandardMetadata):
    slug = models.SlugField(unique=True)
    tour = models.ForeignKey(Tour)
    location = models.ForeignKey(Location)
    artifacts = models.ManyToManyField(Artifact)
    order = models.IntegerField()

    objects = gis_models.GeoManager()

