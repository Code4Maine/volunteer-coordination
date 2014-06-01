from django.template.base import Library

from volunteers.models import VolunteerApplication, Organization

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
    organization = Organization.objects.get(slug=org.slug, managers=user)
    if organization:
        return True
    else:
        return False
