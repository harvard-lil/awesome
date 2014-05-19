from django.contrib.syndication.views import Feed
from awesome.models import Organization, Item

from django.shortcuts import get_object_or_404

from django.http import HttpRequest

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