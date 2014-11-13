from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.template.loader import render_to_string
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from .forms import VolunteerForm, ProjectForm, OrganizationForm, OpportunityForm

from .models import (Opportunity, Project, Organization, Volunteer,
                     VolunteerApplication)
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
            html = render_to_string('volunteers/_opportunity_list.html',
                                    {'object_list': opportunities})
            return HttpResponse(html, mimetype='text/html')


def change_organization(request):
    if 'POST' == request.method:
        new_org = request.POST.get('new_org')
        if new_org:
            current_organization = Organization.objects.get(id=new_org)
            request.session['current_organization'] = current_organization.id
            request.session['{0}_slug'.format(
                'current_organization')] = current_organization.slug
            redirect_url = request.POST.get('redirect_to', '/dashboard')
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect('/dashboard')

class OrganizationMixin(View, views.LoginRequiredMixin):
    org = None
    user_orgs = None

    def dispatch(self, request, *args, **kwargs):
        self.user_orgs = Organization.objects.filter(managers=self.request.user)
        try:
            self.org = self.user_orgs.get(id=self.request.session.get('current_organization'))
        except:
            self.org = None

        if not self.org and self.user_orgs:
            self.org = self.user_orgs[0]
        return super(OrganizationMixin, self).dispatch(request, *args, **kwargs)
    

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


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm


class ProjectListJSONView(JsonView, ListView):
    model = Project
    json_dumps_kwargs = {u"indent": 2}

    def get(self, request, *args, **kwargs):
        context = serializers.serialize('json',
                                        self.get_queryset().all())

        return self.render_json_response(context)


class ProjectListView(JsonView, ListView):
    model = Project


class OpportunityCreateView(CreateView):
    model = Opportunity
    form_class = OpportunityForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = Project.objects.get(slug=self.kwargs['slug'])
            obj.save()
            return HttpResponseRedirect(self.success_url)
        return super(OpportunityCreateView, self).post(request, *args, **kwargs)


class OpportunityVolunteerView(View):
    '''
    Takes a get request to a URL with a volunteer and an 
    and adds the user to the opportunities candidate list.
    '''

    def get(self, request, *args, **kwargs):
        # TODO:
        # 1. Grab user from request
        user = request.user
        if user.is_anonymous():
            return redirect(reverse('account_login'))
        # 2. Check that they can apply to the opportunity in the url
        qs = Opportunity.open_objects.all()
        try:
            slug = kwargs['slug']
            project_slug = kwargs['project_slug']
        except AttributeError:
            slug = project_slug = None

        opp = get_object_or_404(qs, slug=slug, project__slug=project_slug)
        # 3. If so, add a VolunteerApplication
        try:
            application = VolunteerApplication.objects.get(user=user,
                                                           opportunity=opp)
        except VolunteerApplication.DoesNotExist:
            application = None
        if not application:
        
            application = VolunteerApplication.objects.create(user=user,
                                                              opportunity=opp)
            application.save()
        # 4. Notify the lead volunteers and managers of the project and org
        return redirect(reverse('opportunity-detail', kwargs={
            'slug': slug,
            'project_slug': project_slug}))


class OpportunityUnVolunteerView(View):
    '''
    Takes a posted form with a volunteer and an OpportunityDetailJSONView
    and adds the user to the opportunities candidate list.
    '''

    def get(self, request, *args, **kwargs):
        # TODO:
        # 1. Grab user from request
        user = request.user
        # 2. Check that they can apply to the opportunity in the url
        qs = Opportunity.open_objects.all()
        try:
            slug = kwargs['slug']
            project_slug = kwargs['project_slug']
        except AttributeError:
            slug = project_slug = None

        opp = get_object_or_404(qs, slug=slug, project__slug=project_slug)
        # 3. If so, add a VolunteerApplication
        try:
            application = VolunteerApplication.objects.get(user=user,
                                                           opportunity=opp)
            application.delete()
        except VolunteerApplication.DoesNotExist:
            application = None
        return redirect(reverse('opportunity-detail', kwargs={
            'slug': slug,
            'project_slug': project_slug}))


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


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.managers.add(self.request.user)
            obj.save()
            return HttpResponseRedirect(self.success_url)
        return super(OrganizationCreateView, self).post(request, *args, **kwargs)


class DashboardView(OrganizationMixin, DetailView):
    ''' DashboardView
    '''
    model = Volunteer
    template_name = 'volunteers/dashboard.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        context['applications'] = VolunteerApplication.objects.filter(
            user=self.request.user)
        context['org'] = self.org
        context['user_orgs'] = self.user_orgs
        context['org_form'] = OrganizationForm
        return context


class ProfileUpdateView(UpdateView):
    model = Volunteer
    template_name = 'volunteers/profile_update.html'
    form_class = VolunteerForm

    def get_object(self, *args, **kwargs):
        return self.request.user

