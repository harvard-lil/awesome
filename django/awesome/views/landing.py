import logging

from awesome.models import Organization, Item

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db.models import Count, Sum

logger = logging.getLogger(__name__)


def not_found(request):
    """The application-wide 404 page."""
    return render_to_response('404.html', {'user': request.user})

def landing(request):
    """The welcome page."""
    
    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
    
    if 'subdomain' in request.META:
        branch = request.GET.get('branch', '')
        org = Organization.objects.get(slug=request.META['subdomain'])
    
        return render_to_response('landing_org.html', {'user': request.user, 'organization': org,
                                               'branch': branch, 'twitter_username': org.twitter_username,
                                               'ga_key': GOOGLE['ANALYTICS_KEY']})
    else:
        items = Item.objects.values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins')[:5]
        creators = Item.objects.values('creator').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins')[:5]
        logger.debug(items)
        context = {'ga_key': GOOGLE['ANALYTICS_KEY'], 'items': items, 'creators': creators}
               
        context.update(csrf(request))
        return render_to_response('landing_default.html', context)