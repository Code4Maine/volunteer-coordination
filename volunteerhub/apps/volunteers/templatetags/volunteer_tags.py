from django.template.base import Library

from volunteers.models import (VolunteerApplication, Organization,
                               Project)

register = Library()


@register.assignment_tag(takes_context=True)
def application_status(context, opp, user):
    try:
        app = VolunteerApplication.objects.get(user=user,
                                               opportunity=opp)
    except:
        app = None
    if app:
        return app.status
    else:
        return None


@register.assignment_tag(takes_context=True)
def manager_of(context, org, user):
    try:
        organization = Organization.objects.get(slug=org.slug, managers=user)
    except:
        organization = None
    if organization:
        return True
    else:
        return False


@register.assignment_tag(takes_context=True)
def lead_volunteer_of(context, project, user):
    try:
        proj = Project.objects.get(slug=project.slug, lead_volunteers=user)
    except:
        proj = None
    if proj:
        return True
    else:
        return False
