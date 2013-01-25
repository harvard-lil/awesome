from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from awesome.models import Organization, Branch, Item, Checkin
from datetime import datetime
from tastypie import fields
from tastypie.resources import ModelResource, ALL



class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'
        allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()

class BranchResource(ModelResource):
    organization = fields.ToOneField(OrganizationResource, 'organization', full = True )

    class Meta:
        queryset = Branch.objects.all()
        resource_name = 'branch'
        allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()
        
class ItemResource(ModelResource):    
    branch = fields.ToOneField(BranchResource, 'branch', full = True )
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        filtering = {"status": ALL }
        ordering = ['latest_checkin', 'number_checkins']
        allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()
    
        #last_checkin = 'some date'
        #bundle.data['last_checkin'] = last_checkin
        #return bundle

        #for checkins in bundle.obj.checkins.all():
            #bundle.data['self.']
    
#        last_checkin = None
        #for checkin in bundle.obj.checkins.all():
            #bundle.data['last_checkin'] = checkin['checked_in_time']
            
        
        
class CheckinResource(ModelResource):
    
    class Meta:
        queryset = Checkin.objects.all()
        resource_name = 'checkin'