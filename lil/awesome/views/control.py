from lil.awesome.models import Organization
from lil.awesome.forms import OrganizationForm, BranchForm

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

def home(request):
    """Control (user admin site) landing page"""
    
    org = Organization.objects.get(slug=request.META['subdomain'])
    
    context = {
            'user': request.user,
            'organization': org,
        }
    
    return render_to_response('control.html', context)

def org(request):
    """Users can control (admin) their org from here"""

    org = Organization.objects.get(slug=request.META['subdomain'])
    
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

    org = Organization.objects.get(slug=request.META['subdomain'])

    if request.method == 'POST':
        submitted_form = BranchForm(request.POST, instance=org)

        if submitted_form.is_valid():
            submitted_form.save()

            return HttpResponseRedirect(reverse('control_branch'))
        else:
            context = {
                'user': request.user,
                'organization': org,
                'form': submitted_form,
            }
            context.update(csrf(request))    
            return render_to_response('control-branch.html', context)

    else:  
        form = BranchForm(instance=org)
        context = {
            'user': request.user,
            'organization': org,
            'form': form,
        }
        context.update(csrf(request))    
        return render_to_response('control-branch.html', context)