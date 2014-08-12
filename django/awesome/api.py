from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from datetime import datetime

from haystack.query import SearchQuerySet
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from awesome.models import Organization, Branch, Item, Checkin


from tastypie.utils import trailing_slash

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'
        allowed_methods = ['get', 'post']
        filtering = {"slug": ALL }
        excludes = ['service_lookup',
                    'twitter_oauth_secret',
                    'twitter_oauth_token',
                    'worldcat_key',]

class BranchResource(ModelResource):
    organization = fields.ToOneField(OrganizationResource, 'organization', full = True )

    class Meta:
        queryset = Branch.objects.all()
        resource_name = 'branch'
        allowed_methods = ['get']
        filtering = {"organization": ALL_WITH_RELATIONS, "slug": ALL, "lat": ALL }
        
class ItemResource(ModelResource):    
    branch = fields.ToOneField(BranchResource, 'branch', full = True )
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        filtering = {"branch": ALL_WITH_RELATIONS,  'physical_format': ALL }
        ordering = ['latest_checkin', 'number_checkins',]
        allowed_methods = ['get',]
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Item).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
        
class CheckinResource(ModelResource):
    
    class Meta:
        queryset = Checkin.objects.all()
        resource_name = 'checkin'