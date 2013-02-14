from lil.awesome.models import Organization, Item
from django.contrib.sites.models import Site

from django.shortcuts import render_to_response

def widget(request):
    """The widget"""
    
    branch = request.GET.get('branch', '')    
    org = Organization.objects.get(slug=request.META['subdomain'])
    awesome_domain = Site.objects.get_current().domain
    
    if len(branch) != 0:
        items = Item.objects.filter(branch__slug=branch, branch__organization=org).order_by('-latest_checkin')[:5]
    else:
        items = Item.objects.filter(branch__organization=org).order_by('-latest_checkin')[:5]
        

    return render_to_response('widget.js', {'awesome_domain': awesome_domain, 'user': request.user, 'organization': org,
                              'branch': branch, 'items':items}, mimetype='Content-type: text/javascript')