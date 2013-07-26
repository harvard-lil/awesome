from awesome.models import Organization, Branch, Item, Checkin
from awesome.forms import OrganizationForm, BranchForm, AnalyticsForm

import datetime, logging, urlparse

import oauth2 as oauth

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)

try:
    from awesome.local_settings import *
except ImportError, e:
    logger.error('Unable to load local_settings.py:', e)


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
        
        
def branch_edit(request):
    """Users can edit branches here"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)

    if request.method == 'POST':
        submitted_form = BranchForm(request.POST,)

        branch = Branch.objects.get(organization=org, id=request.POST.get('branch-id'))

        if submitted_form.is_valid():
            
            form = BranchForm(request.POST, instance=branch)
            form.save()

            return HttpResponseRedirect(reverse('control_branch'))
        else:
            context = {
                'user': request.user,
                'organization': org,
                'form': submitted_form,
                'branch': branch,
            }
            context.update(csrf(request))    
            return render_to_response('control-branch-edit.html', context)

    else:
        branch = Branch.objects.get(id=request.GET.get('branch-id'), organization=org)
        
        form = BranchForm(instance=branch)

        context = {
            'user': request.user,
            'organization': org,
            'form': form,
            'branch': branch    
        }
        context.update(csrf(request))
        return render_to_response('control-branch-edit.html', context)

def branch_delete(request):
    """Users are presented with the option to delete a branch here"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    org = Organization.objects.get(user=request.user)


    if request.method == 'POST':
        submitted_form = BranchForm(request.POST,)

        branch = Branch.objects.get(organization=org, id=request.POST.get('branch-id'))
        try:
            transfer_branch = Branch.objects.get(organization=org, id=request.POST.get('transfer-branch'))
        except Branch.DoesNotExist:
            transfer_branch = None

        if transfer_branch:
            Item.objects.filter(branch=branch).update(branch=transfer_branch)
        
        branch.delete()
        
        return HttpResponseRedirect(reverse('control_branch'))

    else:

        branch = Branch.objects.get(id=request.GET.get('branch-id'), organization=org)
    
        transfer_branches = Branch.objects.filter(organization=org).exclude(id=branch.id)

        context = {
            'user': request.user,
            'organization': org,
            'branch': branch,
            'transfer_branches': transfer_branches,
        }
        context.update(csrf(request))
        return render_to_response('control-branch-delete.html', context)

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


def twitter_config(request):
    """Users can authorize AB to tweet for them here
    
    In this method and twitter_callback, we manage the three-legged twitter oauth process
    
    Many thanks to https://github.com/simplegeo/python-oauth2 for the example
    """
    
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))

    if request.method == 'POST':
        # A user is reqeusting twitter to auth. we need to get a token here and then redirect
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'
        
        consumer = oauth.Consumer(TWITTER['CONSUMER_KEY'], TWITTER['CONSUMER_SECRET'])
        client = oauth.Client(consumer)
        resp, content = client.request(request_token_url, "GET")

        if resp['status'] != '200':
            logger.warn('Unable to get a 200 response from twitter for oauth integration.')
            logger.warn("Invalid response %s." % resp['status'])
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))
        
        request.session['request_token'] = request_token['oauth_token']
        request.session['request_token_secret'] = request_token['oauth_token_secret']
        request.session.modified = True
        
        return HttpResponseRedirect("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))
        
    else:
        org = Organization.objects.get(user=request.user)

        context = {
            'user': request.user,
            'organization': org,
            'existing_config': False,
        }

        if org.twitter_oauth_token and org.twitter_oauth_secret:
            context['existing_config'] = True;

        context.update(csrf(request))
        return render_to_response('control-twitter-config.html', context)
        
def twitter_callback(request):
    """Twitter will redirect the user to this method after they auth us to tweet
    
        If the redirect contains oauth_token and oauth_token_secret, the user authed us to tweet
        if we don't see these two things, the user cancelled or something went wrong. We should give them that message.
    
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))


    access_token_url = 'https://api.twitter.com/oauth/access_token'

    request_token = request.session['request_token']
    request_token_secret = request.session['request_token_secret']
    
    token = oauth.Token(request_token, request_token_secret)
    token.set_verifier(request.GET.get('oauth_verifier'))
    consumer = oauth.Consumer(TWITTER['CONSUMER_KEY'], TWITTER['CONSUMER_SECRET'])
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    org = Organization.objects.get(user=request.user)

    context = {
        'user': request.user,
        'organization': org,
        'twitter_success': True,
    }
    
    if 'oauth_token' in access_token and 'oauth_token_secret' in access_token:
        org.twitter_username = access_token['screen_name']
        org.twitter_oauth_token = access_token['oauth_token']
        org.twitter_oauth_secret = access_token['oauth_token_secret']
        org.save()
        
        del request.session['request_token']
        del request.session['request_token_secret']
        request.session.modified = True
        
    else:
        context['twitter_success'] = False

    return render_to_response('control-twitter-confirm.html', context)
    
def item_delete(request):
    """
    Occasionally folks want to delete items. We handle that here.
    
    Dump 100 items to the screen each with a delete button. That delete button makes a 
    post back here. We delete the item and then send redirect them back to this view. Crud but works.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))


    org = Organization.objects.get(user=request.user)

    if request.method == 'POST':
        # if post, look for identifier. delete that identifier and its related checkins
        selected_items = request.POST.getlist('items')
        
        for selected_item in selected_items:
            item = Item.objects.get(id=selected_item,branch__organization=org)
            item.delete()

        return HttpResponseRedirect(reverse('control_item_delete'))
        
    else:
        # get branch from GET params
        # get 100 most recent items from specified branch
        
        passed_in_branch_id = request.GET.get('filtered_branch')
        
        org = Organization.objects.get(user=request.user)
        branches = Branch.objects.filter(organization=org)
        
        filter_branch = branches[0]
        
        if passed_in_branch_id:
            filter_branch = Branch.objects.get(id=passed_in_branch_id)
        
        items = Item.objects.filter(branch=filter_branch, branch__organization=org).order_by('-latest_checkin')[:100]

    context = {
        'user': request.user,
        'organization': org,
        'branches': branches,
        'filter_branch_id': filter_branch.id,
        'items': items,
    }
    
    context.update(csrf(request))

    return render_to_response('delete-item.html', context)


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