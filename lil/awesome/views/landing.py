import logging

from lil.awesome.models import Organization

from django.shortcuts import render_to_response
from django.core.context_processors import csrf

logger = logging.getLogger(__name__)


def not_found(request):
    """The application-wide 404 page."""
    return render_to_response('404.html', {'user': request.user})

def landing(request):
    """The welcome page."""
    
    try:
        from lil.awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
    
    if 'subdomain' in request.META:
        branch = request.GET.get('branch', '')
        org = Organization.objects.get(slug=request.META['subdomain'])
    
        return render_to_response('landing_org.html', {'user': request.user, 'organization': org,
                                               'branch': branch, 'twitter_username': org.twitter_username,
                                               'ga_key': GOOGLE['ANALYTICS_KEY']})
    else:
        context = {'ga_key': GOOGLE['ANALYTICS_KEY']}
               
        context.update(csrf(request))
        return render_to_response('landing_default.html', context)