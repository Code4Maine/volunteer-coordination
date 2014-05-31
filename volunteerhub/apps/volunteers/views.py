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
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.template.loader import render_to_string

from .models import Organization, Tour, Task


def get_nearby_tasks(request, *args, **kwargs):
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
        #  TODO: Search close and go out until we find a threshold of tasks
        meters = 5000
        tasks = Task.objects.filter(point__distance_lte=(current_point,D(m=meters)))
        if getattr(request.GET, 'json', False):
            data = serializers.serialize('json', tasks)
            return HttpResponse(data, mimetype='application/json')
        else:
            html = render_to_string('volunteers/_task_list.html', {'object_list':tasks})
            return HttpResponse(html, mimetype='text/html')


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class TaskDetailView(DetailView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(
            organization_slug=self.kwargs['organization-slug'])


class TaskListView(ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(
            organization-_slug=self.kwargs['organization-slug'])


class CreateTaskView(CreateView):
    pass


class UpdateTaskView(CreateView):
    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            artifact_dict = {}
            if self.form.title:
                artifact_dict['title'] = self.form.title
