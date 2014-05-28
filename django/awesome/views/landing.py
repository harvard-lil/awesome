import logging, math

from datetime import date, timedelta
from awesome.models import Organization, Item, Branch

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.db.models import Count, Sum, Q

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
        
        template = 'landing_org_{theme}.html'.format(theme = org.theme)
        
        context = {'user': request.user, 'organization': org,
                                               'branch': branch, 'twitter_username': org.twitter_username,
                                               'ga_key': GOOGLE['ANALYTICS_KEY']}
        context = RequestContext(request, context)
    
        return render_to_response(template, context)
    else:
        items = Item.objects.values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins')[:10]
        creators = Item.objects.values('creator').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').exclude(creator='')[:10]
        
        startdate = date.today() + timedelta(days=1)
        enddate = startdate - timedelta(days=2)
        recently = Item.objects.filter(latest_checkin__gt=enddate,
                                latest_checkin__lt=startdate).order_by('-latest_checkin')
                                
        num_libraries = Organization.objects.count()
        #num_libraries = int(math.floor(num_libraries%5) * 5)
        
        context = {'ga_key': GOOGLE['ANALYTICS_KEY'], 'items': items, 'creators': creators, 'recently': recently, 'num_libraries': num_libraries}
               
        context = RequestContext(request, context)
        return render_to_response('landing_default.html', context)
        

def explorer(request):

    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
        
    items = Item.objects.filter(classifications__name__icontains="teen").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    creators = Item.objects.filter(classifications__name__icontains="children").exclude(classifications__name__icontains="teen").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    scifis = Item.objects.filter(classifications__name__icontains="science fiction").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    comics = Item.objects.filter(Q(classifications__name__icontains="graphic novel") | Q(classifications__name__icontains="comics")).values('title').annotate(total_checkins=Sum('number_checkins', distinct = True)).order_by('-total_checkins')[:10]
    
    context = {'ga_key': GOOGLE['ANALYTICS_KEY'], 'items': items, 'creators': creators, 'scifis': scifis, 'comics': comics}
               
    context = RequestContext(request, context)
    return render_to_response('explorer.html', context)