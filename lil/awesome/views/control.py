from lil.awesome.models import Organization, Branch, Item, Checkin
from lil.awesome.forms import OrganizationForm, BranchForm, AnalyticsForm

import datetime

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
        
        
def analytics(request):
    """Users get counts of awesome things here"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)


    # Get the standard buckets (last 24 hours, last 7 days, ...)
    branches = Branch.objects.filter(organization=org)

    branches_with_counts = []

    last_30 = datetime.datetime.now() + datetime.timedelta(-30)
    last_7 = datetime.datetime.now() + datetime.timedelta(-7)
    last_1 = datetime.datetime.now() + datetime.timedelta(-1)
    
    for branch in branches:
        branch_with_count = {}
        branch_with_count['name'] = branch.name
        branch_with_count['day_one'] = len(Checkin.objects.filter(item__branch=branch))
        branch_with_count['last_30'] = len(Checkin.objects.filter(checked_in_time__gt=last_30, item__branch=branch))
        branch_with_count['last_7'] = len(Checkin.objects.filter(checked_in_time__gt=last_7, item__branch=branch))
        branch_with_count['last_1'] = len(Checkin.objects.filter(checked_in_time__gt=last_1, item__branch=branch))
        branches_with_counts.append(branch_with_count)
    
    context = {
        'user': request.user,
        'organization': org,
        'branches': branches_with_counts,
    }
    

    if request.method == 'POST':
        submitted_form = AnalyticsForm(request.POST,)

        if submitted_form.is_valid():
            
            branches_with_counts = []

            start_date = submitted_form.cleaned_data['start_date']
            end_date = submitted_form.cleaned_data['end_date']

            for branch in branches:
                branch_with_count = {}
                branch_with_count['name'] = branch.name
                branch_with_count['query_range'] = len(Checkin.objects.filter(checked_in_time__range=(start_date, end_date), item__branch=branch))
                branches_with_counts.append(branch_with_count)
            
            context['query_branch'] = branches_with_counts
            context['supplied_start'] = start_date
            context['supplied_end'] = end_date
            context['form'] = submitted_form
            context.update(csrf(request))
            return render_to_response('control-analytics.html', context)
        else:
            context['form'] = submitted_form
            context.update(csrf(request))    
            return render_to_response('control-analytics.html', context)
    else:
        
        context['form'] = AnalyticsForm()
        context.update(csrf(request))    
        return render_to_response('control-analytics.html', context)

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