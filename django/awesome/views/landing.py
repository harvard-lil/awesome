import logging, math

from datetime import date, timedelta
from awesome.models import Organization, Item, Branch, Checkin, Shelf, ShelfItem

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.db.models import Count, Sum, Q
from django.contrib.sites.models import Site
from django.http import Http404  

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
        branch_slug = request.GET.get('branch', '')
        if branch_slug:
            try:
                branch = Branch.objects.get(slug=branch_slug, organization__slug=request.META['subdomain'])
            except:
                raise Http404  
        else:
            branch = None
        org = Organization.objects.get(slug=request.META['subdomain'])
        num_items = Item.objects.filter(branch__organization=org).count()
        logger.debug(branch)
        if org.is_active:
        
            template = 'landing_org_{theme}.html'.format(theme = org.theme)
            
            context = {'user': request.user, 'organization': org,
                                                   'branch': branch, 
                                                   'num_items': num_items,'twitter_username': org.twitter_username,
                                                   'ga_key': GOOGLE['ANALYTICS_KEY']}
        
        else:
            template = 'landing_org_deactivated.html'
            awesome_domain = Site.objects.get_current().domain
            context = {'awesome_domain': awesome_domain, 'ga_key': GOOGLE['ANALYTICS_KEY']}
            
        if request.method == 'POST':
            org.cover_service = 'openlibrary'
            org.save()
            return render_to_response(template, context)
    
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
        
def landing_goodbye(request):
    """The welcome page."""
    
    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
    
    if 'subdomain' in request.META:
        branch_slug = request.GET.get('branch', '')
        if branch_slug:
            try:
                branch = Branch.objects.get(slug=branch_slug, organization__slug=request.META['subdomain'])
            except:
                raise Http404  
        else:
            branch = None
        org = Organization.objects.get(slug=request.META['subdomain'])
        num_items = Item.objects.filter(branch__organization=org).count()
        logger.debug(branch)
        if org.is_active:
        
            template = 'landing_org_{theme}.html'.format(theme = org.theme)
            
            context = {'user': request.user, 'organization': org,
                                                   'branch': branch, 
                                                   'num_items': num_items,'twitter_username': org.twitter_username,
                                                   'ga_key': GOOGLE['ANALYTICS_KEY']}
        
        else:
            template = 'landing_org_deactivated.html'
            awesome_domain = Site.objects.get_current().domain
            context = {'awesome_domain': awesome_domain, 'ga_key': GOOGLE['ANALYTICS_KEY']}
            
        if request.method == 'POST':
            org.cover_service = 'openlibrary'
            org.save()
            return render_to_response(template, context)
    
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
        return render_to_response('landing_goodbye.html', context)
        

def shelf(request, shelf_slug):
    """The welcome page."""
    
    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
    
    if 'subdomain' in request.META:
        try:
        	shelf = Shelf.objects.get(slug=shelf_slug, organization__slug=request.META['subdomain'])
        except:
        	raise Http404  

        org = Organization.objects.get(slug=request.META['subdomain'])
        items = ShelfItem.objects.filter(shelf = shelf).order_by('-sort_order')

        if org.is_active:
        
            template = 'shelf.html'
            
            context = {'user': request.user, 'organization': org, 'shelf': shelf, 'items': items}
        
        else:
            template = 'landing_org_deactivated.html'
            awesome_domain = Site.objects.get_current().domain
            context = {'awesome_domain': awesome_domain, 'ga_key': GOOGLE['ANALYTICS_KEY']}
    
        context = RequestContext(request, context)
        return render_to_response(template, context)
    else:
        raise Http404 
        

def explorer(request):

    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
        
    items = Item.objects.filter(classifications__name__icontains="teen").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    creators = Item.objects.filter(classifications__name__icontains="children").exclude(classifications__name__icontains="teen").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    scifis = Item.objects.filter(classifications__name__icontains="science fiction").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    comics = Item.objects.filter(Q(classifications__name__icontains="graphic novel") | Q(classifications__name__icontains="comics")).values('title').annotate(total_checkins=Sum('number_checkins', distinct = True)).order_by('-total_checkins')[:10]
    
    search_results = None
    search_query = None
    # handle search
    search_query = request.GET.get('query', '')
    if search_query:
        search_results = Item.objects.filter(classifications__name__icontains=search_query).values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    context = {'ga_key': GOOGLE['ANALYTICS_KEY'], 'items': items, 'creators': creators, 'scifis': scifis, 'comics': comics, 'search_results': search_results, 'query': search_query}
               
    context = RequestContext(request, context)
    return render_to_response('explorer.html', context)
    
    
def discover(request):

    try:
        from awesome.local_settings import *
    except ImportError, e:
        logger.error('Unable to load local_settings.py:', e)
        
    items = Item.objects.filter(classifications__name__icontains="teen").values('title', 'creator').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    creators = Item.objects.filter(classifications__name__icontains="children").exclude(classifications__name__icontains="teen").values('title').annotate(total_checkins=Sum('number_checkins')).order_by('-total_checkins').distinct()[:10]
    
    startdate = date.today() + timedelta(days=1)
    enddate = startdate - timedelta(days=30)
    
    scifis = Checkin.objects.filter(item__classifications__name__icontains="science fiction", checked_in_time__gt=enddate, checked_in_time__lt=startdate).values('item__title').annotate(total_checkins=Count('item')).order_by('-total_checkins')[:10]
    
    logger.debug(scifis)
    
    comics = Item.objects.filter(Q(classifications__name__icontains="graphic novel") | Q(classifications__name__icontains="comics")).values('title').annotate(total_checkins=Sum('number_checkins', distinct = True)).order_by('-total_checkins')[:10]
    
    context = {'ga_key': GOOGLE['ANALYTICS_KEY'], 'items': items, 'creators': creators, 'scifis': scifis, 'comics': comics}
               
    context = RequestContext(request, context)
    return render_to_response('discover.html', context)