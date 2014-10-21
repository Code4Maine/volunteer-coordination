from .models import Organization

def organization_loader(request):
    current_org = request.session.get('current_organization', None)
    try:
        user_orgs = Organization.objects.filter(managers=request.user)
    except TypeError:
        user_orgs = []
    # If current_organization is blank and a user only has one org,
    # pick it. Otherwise, don't mess with current_org
    if len(user_orgs) >= 1 and current_org is None:
        current_org = user_orgs[0]
    return {'current_organization': current_org, 'user_orgs': user_orgs}
