import logging

from django.contrib.syndication.views import Feed
from awesome.models import Organization, Item, Branch

from django.shortcuts import get_object_or_404

from django.http import HttpRequest

logger = logging.getLogger(__name__)

class LatestEntriesFeed(Feed):
    
    def get_object(self, request):
        return get_object_or_404(Organization, slug=request.META['subdomain'])
        
    def link(self, obj):
    		return 'http://' + org.slug + '.awesomebox.io'
        
    def title(self, obj):
        return 'Recently Awesome at ' + obj.name
        
    def description(self, obj):
    		return 'Keep up with the latest awesome items at ' + obj.name
        
    def link(self, obj):
        return 'http://' + obj.slug + '.awesomebox.io/'

    def items(self, obj):
        result = Item.objects.filter(branch__organization=obj).order_by('-latest_checkin')[:15]
        for entry in result:
            entry.slug = obj.slug
        return result
        
    def get_org(self, obj):
        return self

    def item_title(self, item):
        return item.title

    def item_description(self, item):
    	if item.cover_art:
    		return '<img class="item-cover" src="' + item.cover_art + '" />' + item.title + ' by ' + item.creator
    	else:
    	  if item.isbn:
    	    return '<img src="http://covers.openlibrary.org/b/isbn/' + item.isbn + '-M.jpg" />' + item.title + ' by ' + item.creator
    	  else:
    	    return item.title + ' by' + item.creator

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        library = get_object_or_404(Organization, slug=item.slug)
        value = ''
        if library.catalog_query == 'isbn':
          value = item.catalog_id
        elif library.catalog_query == 'title':
          value = item.title
        elif library.catalog_query == 'titleauthor':
          value = item.title + '+' + item.creator
        elif library.catalog_query == 'landing' or library.catalog_query == 'notset':
            value = ''
        return library.catalog_base_url + value
        
        
class BranchLatestEntriesFeed(Feed):
    
    def get_object(self, request, branch_slug):
        return Branch.objects.get(organization__slug=request.META['subdomain'], slug=branch_slug)
        
    def link(self, obj):
    		return 'http://' + obj.organization.slug + '.awesomebox.io'
        
    def title(self, obj):
        return 'Recently Awesome at ' + obj.organization.name + ' ' + obj.name + ' branch'
        
    def description(self, obj):
    		return 'Keep up with the latest awesome items at ' + obj.organization.name + ' ' + obj.name + ' branch'
        
    def link(self, obj):
        return 'http://' + obj.organization.slug + '.awesomebox.io/'

    def items(self, obj):
        result = Item.objects.filter(branch=obj.id).order_by('-latest_checkin')[:15]
        for entry in result:
            entry.slug = obj.organization.slug
        return result

    def item_title(self, item):
        return item.title

    def item_description(self, item):
    	if item.cover_art:
    		return '<img class="item-cover" src="' + item.cover_art + '" />' + item.title + ' by ' + item.creator
    	else:
    	  if item.isbn:
    	    if item.branch.organization.cover_service == 'openlibrary' or item.branch.organization.cover_service == 'notset':
                return '<img src="http://covers.openlibrary.org/b/isbn/' + item.isbn + '-M.jpg" />' + item.title + ' by ' + item.creator
            elif item.branch.organization.cover_service == 'syndetic':
                return '<img src="http://www.syndetics.com/index.php?isbn=' + item.isbn + '/mc.gif&client=' + object.branch.organization.cover_user_id + '" />' + item.title + ' by ' + item.creator
            elif item.branch.organization.cover_service == 'tlc':
                return '<img src="http://content.tlcdelivers.com/tlccontent?customerid=' + item.branch.organization.cover_user_id + '&requesttype=bookjacket-md&isbn=' + item.isbn + '" />' + item.title + ' by ' + item.creator
            elif item.branch.organization.cover_service == 'contentcafe':
                return '<img src="http://contentcafe2.btol.com/ContentCafe/Jacket.aspx?&userID=' + item.branch.organization.cover_user_id + '&password=' + item.branch.organization.cover_password + '&Value=' + item.isbn + '&content=M&Return=1&Type=M' + '" />' + item.title + ' by ' + item.creator
    	  else:
    	    return '<img src="static/images/grey-cover.png" />' + item.title + ' by ' + item.creator

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        library = get_object_or_404(Organization, slug=item.slug)
        value = ''
        if library.catalog_query == 'isbn':
          value = item.catalog_id
        elif library.catalog_query == 'title':
          value = item.title
        elif library.catalog_query == 'titleauthor':
          value = item.title + '+' + item.creator
        elif library.catalog_query == 'landing' or library.catalog_query == 'notset':
            value = ''
        return library.catalog_base_url + value