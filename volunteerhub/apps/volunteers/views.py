# Views here are heavily modified from traditional Django views
# Instead of using the ORM, we're going to hack up a Riak interface
# So that artifact data is stored there instead of the default DB
#import riak
import uuid
import time
import urllib

from django.core import serializers
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, View
#from riak_crud import get_artifact, create_artifact
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.template.loader import render_to_string

from .models import Organization, Tour, Artifact

class WhatsHereView(ListView):
    model = Artifact
    template_name = 'artifacts/whats_here.html'

    def get_context_data(self, **kwargs):
        context = super(WhatsHereView, self).get_context_data(**kwargs)
        # Here we need to do our geo lookup of artifacts based on our 
        # current location given to us by the browser
        context['artifacts'] = context['object_list'] = Artifact.objects.filter()
        return context

def get_nearby_artifacts(request, *args, **kwargs):
    if kwargs['lat'] and kwargs['lng']:
        if kwargs['lat'][0] == '-':
            lat = kwargs['lat'][:3] + '.' + kwargs['lat'][3:]
        else:
            lat = kwargs['lat'][:2] + '.' + kwargs['lat'][2:]
        if kwargs['lng'][0] == '-':
            lng = kwargs['lng'][:3] + '.' + kwargs['lng'][3:]
        else:
            lng = kwargs['lng'][:2] + '.' + kwargs['lng'][2:]

        current_point = GEOSGeometry('POINT(%s %s)' % (lat, lng))
        #  TODO: Search close and go out until we find a threshold of artifacts
        meters = 5000
        artifacts = Artifact.objects.filter(point__distance_lte=(current_point,D(m=meters)))
        if getattr(request.GET, 'json', False):
            data = serializers.serialize('json', artifacts)
            return HttpResponse(data, mimetype='application/json')
        else:
            html = render_to_string('artifacts/_artifact_list.html', {'object_list':artifacts})
            return HttpResponse(html, mimetype='text/html')

class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class ArtifactDetailView(DetailView):
    model = Artifact

    def get_queryset(self, *args, **kwargs):
        return Artifact.objects.filter(organization__slug=self.kwargs['organization_slug'])


class ArtifactListView(ListView):
    model = Artifact

    def get_queryset(self, *args, **kwargs):
        return Artifact.objects.filter(organization__slug=self.kwargs['organization_slug'])


class TourListView(ListView):
    model = ListView

    def get_queryset(self, *args, **kwargs):
        return Tour.objects.filter(organization__slug=self.kwargs['organization_slug'])


class TourDetailView(DetailView):
    model = DetailView

    def get_queryset(self, *args, **kwargs):
        return Tour.objects.filter(organization__slug=self.kwargs['organization_slug'])


class CreateArtifactView(CreateView):
    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            encoded_image = urllib.quote(open(self.form.image.url, "rb").read().encode("base64"))
            artifact_dict = {
                'title': self.form.title,
                'description': self.form.description,
                'address': self.form.address,
                'city': self.form.city,
                'state': self.form.state,
                'zipcode': self.form.zipcode,
                'image': encoded_image,
                'created': time.time(),
                'updated': time.time(),
                'created_by': request.user.username,
            }
            create_artifact(artifact_dict)

class UpdateArtifactView(CreateView):
    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            artifact_dict = {}
            if self.form.title:
                artifact_dict['title'] = self.form.title
