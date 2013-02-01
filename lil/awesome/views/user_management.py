import logging

from lil.awesome.models import Organization, Branch
from lil.awesome.forms import UserRegForm

from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib import auth

logger = logging.getLogger(__name__)

try:
    from lil.awesome.local_settings import *
except ImportError, e:
    logger.error('Unable to load local_settings.py:', e)


def process_register(request):
    """Register a new user"""
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':

        reg_key = request.POST.get('reg_key', '')
        
        # We only want folks we know and trust with our key to create new AB accounts
        if not reg_key or reg_key != INTERNAL['REG_KEY']:
            return HttpResponseRedirect(reverse('landing'))
        
        
        form = UserRegForm(request.POST)
        if form.is_valid():
            new_user = form.save()
                        
            # Log the user in
            supplied_username = request.POST.get('username', '')
            supplied_password = request.POST.get('password', '')
            user = auth.authenticate(username=supplied_username, password=supplied_password)
            auth.login(request, user)
            
            supplied_org_name = request.POST.get('organization_name', '')
            supplied_org_slug = request.POST.get('organization_slug', '')
            supplied_service_lookup = request.POST.get('service_lookup', '')
            supplied_catalog_base_url = request.POST.get('catalog_base_url', '')
                        
            org = Organization(user=user,
                               name=supplied_org_name,
                               slug=supplied_org_slug,
                               service_lookup=supplied_service_lookup,
                               catalog_base_url=supplied_catalog_base_url,)
            org.save()
            
            supplied_branch_name = request.POST.get('branch_name', '')
            supplied_branch_slug = request.POST.get('branch_slug', '')

            
            branch = Branch(organization=org,
                            name=supplied_branch_name,
                            slug=supplied_branch_slug,)
            branch.save()
            
            return HttpResponseRedirect(reverse('landing'))
        else:
            c.update({'form': form})
            return render_to_response('register.html', c)
    else:
        form = UserRegForm()
        c.update({'form': form})
        return render_to_response("register.html", c)