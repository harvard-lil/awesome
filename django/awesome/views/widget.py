from awesome.models import Organization, Item
from django.contrib.sites.models import Site

from django.shortcuts import get_object_or_404, render_to_response

def widget(request):
    """The widget"""
    
    branch = request.GET.get('branch', '')
    style = request.GET.get('style', '') 
    org = Organization.objects.get(slug=request.META['subdomain'])
    awesome_domain = Site.objects.get_current().domain
    
    if len(branch) != 0:
        items = Item.objects.filter(branch__slug=branch, branch__organization=org).order_by('-latest_checkin')[:5]
    else:
        items = Item.objects.filter(branch__organization=org).order_by('-latest_checkin')[:5]
        

    return render_to_response('widget.js', {'awesome_domain': awesome_domain, 'user': request.user, 'organization': org,
                              'branch': branch, 'items':items, 'style': style}, mimetype='Content-type: text/javascript')
                              
def catalog_include(request, isbn):
    
    org = get_object_or_404(Organization, slug=request.META['subdomain'])
    item_count = Item.objects.filter(isbn=isbn, branch__organization=org).count()
    awesome_domain = Site.objects.get_current().domain   
        
    return render_to_response('catalog_include.js', {'awesome_domain': awesome_domain, 'item_count': item_count}, mimetype='Content-type: text/javascript')