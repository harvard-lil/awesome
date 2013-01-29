from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from awesome.models import Organization, Branch, Item, Checkin
from datetime import datetime
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS



class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'
        allowed_methods = ['get', 'post']
        filtering = {"slug": ALL }
        authentication = Authentication()
        authorization = Authorization()
        excludes = ['service_lookup',
                    'twitter_consumer_key',
                    'twitter_consumer_secret',
                    'twitter_oauth_secret',
                    'twitter_oauth_token',
                    'worldcat_key',]

class BranchResource(ModelResource):
    organization = fields.ToOneField(OrganizationResource, 'organization', full = True )

    class Meta:
        queryset = Branch.objects.all()
        resource_name = 'branch'
        allowed_methods = ['get', 'post']
        filtering = {"organization": ALL_WITH_RELATIONS, "slug": ALL }
        authentication = Authentication()
        authorization = Authorization()
        
class ItemResource(ModelResource):    
    branch = fields.ToOneField(BranchResource, 'branch', full = True )
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        filtering = {"branch": ALL_WITH_RELATIONS }
        ordering = ['latest_checkin', 'number_checkins']
        allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()


        
        
class CheckinResource(ModelResource):
    
    class Meta:
        queryset = Checkin.objects.all()
        resource_name = 'checkin'