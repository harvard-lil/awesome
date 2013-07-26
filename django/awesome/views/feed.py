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
        return Item.objects.filter(branch__organization=obj).order_by('-latest_checkin')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
    	if item.cover_art:
    		return '<img class="item-cover" src="' + item.cover_art + '" />' + item.title + ' by ' + item.creator
    	else:
    		return '<img src="http://covers.openlibrary.org/b/isbn/' + item.isbn + '-M.jpg" />' + item.title + ' by ' + item.creator

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return 'http://awesomebox.io'