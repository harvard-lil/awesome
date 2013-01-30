from awesome.models import Organization, OrganizationForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

def admin_home(request):
    """Admin landing page"""
    
    org = Organization.objects.get(slug=request.subdomain)
    
    context = {
            'user': request.user,
            'organization': org,
        }
    
    return render_to_response('admin.html', context)

def org(request):
    """Users can admin their org from here"""
    
    branch = request.GET.get('branch', '')
    
    org = Organization.objects.get(slug=request.subdomain)
    
    
    if request.method == 'POST':
        submitted_form = OrganizationForm(request.POST, instance=org)
        
        if submitted_form.is_valid():
            submitted_form.save()
            return HttpResponseRedirect(reverse('useradmin_org'))
    else:  
        
        form = OrganizationForm(instance=org)
        context = {
            'user': request.user,
            'organization': org,
            'form': form,
        }
        context.update(csrf(request))    
        return render_to_response('admin-org.html', context)