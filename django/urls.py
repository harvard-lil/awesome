from awesome.api import OrganizationResource, BranchResource, ItemResource, CheckinResource

from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(OrganizationResource())
v1_api.register(BranchResource())
v1_api.register(ItemResource())
v1_api.register(CheckinResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    
    # Common Pages
    url(r'^', include('awesome.urls')),
)