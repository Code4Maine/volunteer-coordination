from django.core import serializers
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, View
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.template.loader import render_to_string
from django.core import serializers

from .models import Opportunity, Project
from braces import views


def get_nearby_opportunities(request, *args, **kwargs):
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
        #  TODO: Search close and go out until we find a
        #  threshold of opportunities
        meters = 5000
        opportunities = Opportunity.objects.filter(
            point__distance_lte=(current_point, D(m=meters)))
        if getattr(request.GET, 'json', False):
            data = serializers.serialize('json', opportunities)
            return HttpResponse(data, mimetype='application/json')
        else:
            html = render_to_string('projects/_task_list.html',
                                    {'object_list': opportunities})
            return HttpResponse(html, mimetype='text/html')


class JsonView(views.CsrfExemptMixin,
               views.JsonRequestResponseMixin,
               views.JSONResponseMixin, View):
    pass


class ProjectDetailJSONView(JsonView, DetailView):
    model = Project
    json_dumps_kwargs = {u"indent": 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context_dict = {
            u"title": self.object.title,
            u"description": self.object.description
        }

        return self.render_json_response(context_dict)


class ProjectDetailView(JsonView, DetailView):
    model = Project


class ProjectListJSONView(JsonView, ListView):
    model = Project
    json_dumps_kwargs = {u"indent": 2}

    def get(self, request, *args, **kwargs):
        context = serializers.serialize('json',
                                        self.get_queryset().all())

        return self.render_json_response(context)


class ProjectListView(JsonView, ListView):
    model = Project


class OpportunityDetailJSONView(JsonView, DetailView):
    model = Opportunity
    json_dumps_kwargs = {u"indent": 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context_dict = {
            u"title": self.object.title,
            u"description": self.object.description
        }
        self.object = self.get_object()

        return self.render_json_response(context_dict)


class OpportunityDetailView(JsonView, DetailView):
    model = Opportunity
    json_dumps_kwargs = {u"indent": 2}


class CreateOpportunityView(CreateView):
    pass

