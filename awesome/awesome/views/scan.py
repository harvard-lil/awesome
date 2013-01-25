from awesome.models import Organization, Branch
from django.shortcuts import render_to_response

"""
If it's a simple view, let's put it here
"""

def scan(request):
    """Our scan page"""
    org_name = request.subdomain
    branch = request.GET.get('branch')
    
    org = Organization.objects.get(name=org_name)
    branches = Branch.objects.filter(organization=org)
    
    
    return render_to_response('scan.html', {'user': request.user, 'organization': request.subdomain, 'branches': branches})