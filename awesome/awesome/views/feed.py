from awesome.models import Organization, Item
from django.shortcuts import render_to_response

def feed(request):
    """The rss feed"""
    
    branch = request.GET.get('branch', '')    
    org = Organization.objects.get(slug=request.subdomain)
    
    if len(branch) != 0:
        items = Item.objects.filter(branch__slug=branch, branch__organization=org)[:20]
    else:
        items = Item.objects.filter(branch__organization=org)[:20]
        

    return render_to_response('feed.xml', {'user': request.user, 'organization': org,
                              'branch': branch, 'items':items}, mimetype='Content-type: text/xml')