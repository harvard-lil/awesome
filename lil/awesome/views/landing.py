from lil.awesome.models import Organization

from django.shortcuts import render_to_response


def not_found(request):
    """The application-wide 404 page."""
    return render_to_response('404.html', {'user': request.user})

def landing(request):
    """The welcome page."""
    
    if 'subdomain' in request.META:
        branch = request.GET.get('branch', '')
        org = Organization(slug=request.META['subdomain'])
    
        return render_to_response('landing_org.html', {'user': request.user, 'organization': request.META['subdomain'],
                                               'branch': branch, 'twitter_username': org.twitter_username})
    else:
        return render_to_response('landing_default.html')