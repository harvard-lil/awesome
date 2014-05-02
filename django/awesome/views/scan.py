from awesome.models import Organization, Branch

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf


def scan(request):
    """Our scan page"""
    
    if not request.user.is_authenticated():
        url = "%s?next=%s" % (reverse('auth_login'), request.path)
        return HttpResponseRedirect(url)
    
    
    branch = request.GET.get('branch')
    org = Organization.objects.get(user=request.user)
    branches = Branch.objects.filter(organization=org)

    context = {'user': request.user,
               'organization': org,
               'branches': branches}
               
    context = RequestContext(request, context)
    
    return render_to_response('scan.html', context)