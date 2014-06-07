from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import (TitleSlugDescriptionModel,
                                         TimeStampedModel)
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from .utils import get_lat_long


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


#class Skill(TaggedItemBase):
#    pass


class Organization(TimeStampedModel, TitleSlugDescriptionModel):
    phone = PhoneNumberField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    managers = models.ManyToManyField(get_user_model(),
                                      blank=True,
                                      null=True)

    objects = gis_models.GeoManager()

    @permalink
    def get_absolute_url(self):
        return ('project-list', None, {})

    def __unicode__(self):
        return u'{0}'.format(self.title)


class LaborType(TitleSlugDescriptionModel):
    pass

    @permalink
    def get_absolute_url(self):
        return ('opportunity-type', None, {'slug': self.slug})

    def __unicode__(self):
        return u'{0}'.format(self.title)


class Project(TimeStampedModel, TitleSlugDescriptionModel):
    lead_volunteers = models.ManyToManyField(get_user_model(),
                                             blank=True,
                                             null=True)
    organization = models.ForeignKey(Organization, related_name='projects')
    image = models.ImageField(upload_to="project_images",
                              blank=True,
                              null=True)

    @permalink
    def get_absolute_url(self):
        return ('project-detail', None, {'slug': self.slug})

    def __unicode__(self):
        return u'{0} at {1}'.format(self.title, self.organization)


class OpenOpportunityManager(models.Manager):
    def get_queryset(self):
        return super(OpenOpportunityManager, self).get_queryset().filter(
            fulfilled=False)


class Opportunity(TimeStampedModel, TitleSlugDescriptionModel):
    project = models.ForeignKey(Project)
    location = models.ForeignKey(Location, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    labor_type = models.ForeignKey(LaborType, blank=True, null=True)
    fulfilled = models.BooleanField(default=False)
    max_applicants = models.IntegerField(_('Max applicants'), blank=True,
                                         null=True)

    requirements = TaggableManager()

    objects = gis_models.GeoManager()
    open_objects = OpenOpportunityManager()

    @permalink
    def get_absolute_url(self):
        return (
            'opportunity-detail',
            None,
            {'project_slug': self.project.slug, 'slug': self.slug})

    def __unicode__(self):
        return u'{0} for {1}'.format(self.title, self.project)

    @property
    def location(self):
        if len(self.locations.all()) == 1:
            return self.locations.all()[0]
        else:
            return False

    @property
    def app_count(self):
        return len(VolunteerApplication.objects.filter(
            opportunity=self))


class Volunteer(TimeStampedModel):
    '''
    '''
    name = models.CharField(_('Name'), max_length=255)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(blank=True, null=True,
                               max_length=255)
    user = models.ForeignKey(get_user_model(), blank=True, null=True)

    opportunities_completed = models.ManyToManyField(Opportunity,
                                                     blank=True,
                                                     null=True)

    @property
    def is_manager(self):
        if self.organization_set.all():
            return True
        else:
            return False

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @permalink
    def get_absolute_url(self):
        return ('dashboard')


APP_STATUSES = (('pending', 'Pending'),
                ('approved', 'Approved'),
                ('denied', 'Denied'))


def create_volunteer_profile(sender, instance, created, **kwargs):
    if created:
        Volunteer.objects.create(user=instance)

post_save.connect(create_volunteer_profile, sender=get_user_model())


class VolunteerApplication(TimeStampedModel):

    user = models.ForeignKey(get_user_model())
    opportunity = models.ForeignKey(Opportunity)
    status = models.CharField(_('Status'),
                              choices=APP_STATUSES,
                              default='pending',
                              max_length=15)

    def __unicode__(self):
        return u'Application for {0}: {1}'.format(self.opportunity, self.user)
