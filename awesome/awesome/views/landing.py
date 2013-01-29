from awesome.models import Organization
from django.shortcuts import render_to_response

"""
If it's a simple view, let's put it here
"""

def not_found(request):
    """The application-wide 404 page."""
    return render_to_response('404.html', {'user': request.user})

def landing(request):
    """The welcome page."""
    
    branch = request.GET.get('branch', '')
    
    org = Organization(slug=request.subdomain)
    
    return render_to_response('landing.html', {'user': request.user, 'organization': request.subdomain,
                                               'branch': branch, 'twitter_username': org.twitter_username})