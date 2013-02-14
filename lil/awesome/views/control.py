from lil.awesome.models import Organization, Branch
from lil.awesome.forms import OrganizationForm, BranchForm

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

def home(request):
    """Control (user admin site) landing page"""
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)
    
    context = {
            'user': request.user,
            'organization': org,
        }
    
    return render_to_response('control.html', context)

def org(request):
    """Users can control (admin) their org from here"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)
    
    if request.method == 'POST':
        submitted_form = OrganizationForm(request.POST, instance=org)
        
        if submitted_form.is_valid():
            submitted_form.save()

            return HttpResponseRedirect(reverse('control_org'))
        else:
            context = {
                'user': request.user,
                'organization': org,
                'form': submitted_form,
            }
            context.update(csrf(request))    
            return render_to_response('control-org.html', context)
            
    else:  
        form = OrganizationForm(instance=org)
        context = {
            'user': request.user,
            'organization': org,
            'form': form,
        }
        context.update(csrf(request))    
        return render_to_response('control-org.html', context)
        
def branch(request):
    """Users can add branches from here"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)

    if request.method == 'POST':
        submitted_form = BranchForm(request.POST,)

        if submitted_form.is_valid():
            branch = submitted_form.save(commit=False)
            branch.organization = org
            branch.save()

            return HttpResponseRedirect(reverse('control_branch'))
        else:
            branches = Branch.objects.filter(organization=org)
            
            context = {
                'user': request.user,
                'organization': org,
                'branches': branches,
                'form': submitted_form,
            }
            context.update(csrf(request))    
            return render_to_response('control-branch.html', context)

    else:
        form = BranchForm()
        
        branches = Branch.objects.filter(organization=org)
        context = {
            'user': request.user,
            'organization': org,
            'branches': branches,
            'form': form,
            
        }
        context.update(csrf(request))    
        return render_to_response('control-branch.html', context)
        
def widget(request):
    """Users can grab widget code here"""
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)
    awesome_domain = Site.objects.get_current().domain
    
    context = {
            'user': request.user,
            'organization': org,
            'awesome_domain': awesome_domain,
        }
    
    return render_to_response('control-widget.html', context)