import logging

from awesome.models import Organization, Branch
from awesome.forms import (
    UserRegForm, 
    BranchForm, 
    OrganizationFormRegistration, 
    OrganizationFormSelfRegistration
)

from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.sites.models import Site
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    from awesome.local_settings import *
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
        
        
        user_reg_form = UserRegForm(request.POST, prefix = "a")
        org_form = OrganizationFormRegistration(request.POST, prefix = "b")
        branch_form = BranchForm(request.POST, prefix = "c")
        
        if user_reg_form.is_valid() and org_form.is_valid() and branch_form.is_valid():
            new_user = user_reg_form.save()
            new_org = org_form.save(commit=False)
            new_branch = branch_form.save(commit=False)
        
            new_org.user = new_user
            new_org.save()
            
            new_branch.organization = new_org
            new_branch.save()

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)
            
            return HttpResponseRedirect(reverse('landing'))
        
        else:
            c.update({'user_reg_form': user_reg_form,
                      'org_form': org_form,
                      'branch_form': branch_form})
            c = RequestContext(request, c)
                      
            return render_to_response('register.html', c)
    else:
        user_reg_form = UserRegForm(prefix = "a")
        org_form = OrganizationFormRegistration(prefix = "b")
        branch_form = BranchForm(prefix = "c")
        
        c.update({'user_reg_form': user_reg_form,
                  'org_form': org_form,
                  'branch_form': branch_form})
        c = RequestContext(request, c)
        return render_to_response("register.html", c)
        
        
def process_self_register(request):
    """A new user registers"""
    c = {}
    c.update(csrf(request))
    awesome_domain = Site.objects.get_current().domain

    if request.method == 'POST':
 
        user_reg_form = UserRegForm(request.POST, prefix = "a")
        org_form = OrganizationFormSelfRegistration(request.POST, prefix = "b")
        
        if user_reg_form.is_valid() and org_form.is_valid():
            new_user = user_reg_form.save()
            new_org = org_form.save(commit=False)
        
            new_org.user = new_user
            new_org.catalog_query = 'notset'
            new_org.save()
            new_branch = Branch.objects.create(organization=new_org, name="Main", slug="main")
            new_branch.save()
            
            host = request.get_host()

            if settings.DEBUG == False:
              host = settings.HOST
        
            content = '''Welcome to Awesome Box!  To login into your account, visit your login page.
        
http://{slug}.{host}/login
            
For help getting started, visit the help page.
            
http://{slug}.{host}/control/help
            
Happy Awesome-ing!
        
'''.format(slug=new_org.slug, host=host)
        
            logger.debug(content)
        
            send_mail(
                "Your library is about to get more Awesome",
                content,
                settings.DEFAULT_FROM_EMAIL,
                [new_user.email], fail_silently=False
            )

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)
            
            messages.add_message(request, messages.INFO, 'Success! Time to get more Awesome.')
            return HttpResponseRedirect(reverse('auth_login'))
        
        else:
            c.update({'user_reg_form': user_reg_form,
                      'org_form': org_form})
            c = RequestContext(request, c)
                      
            return render_to_response('self_register.html', c)
    else:
        user_reg_form = UserRegForm(prefix = "a")
        org_form = OrganizationFormSelfRegistration(prefix = "b")
        
        c.update({'awesome_domain': awesome_domain, 'user_reg_form': user_reg_form,
                  'org_form': org_form})
        c = RequestContext(request, c)
        return render_to_response("self_register.html", c)