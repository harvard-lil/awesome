from awesome.models import Organization, Branch
from django.http import HttpResponse
from django.shortcuts import render_to_response

"""
If it's a simple view, let's put it here
"""

def scan(request):
    """Our scan page"""
    
    if not request.user.is_authenticated():
        return HttpResponse('You need to authenticate to connect to this resource', status=401)
    
    org_name = request.subdomain
    branch = request.GET.get('branch')
    print org_name
    org = Organization.objects.get(slug=org_name)
    branches = Branch.objects.filter(organization=org)
    
    
    return render_to_response('scan.html', {'user': request.user, 'organization': request.subdomain, 'branches': branches})