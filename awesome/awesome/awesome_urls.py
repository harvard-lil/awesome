from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('awesome.views',

    # Common Pages
    url(r'^$', 'welcome.welcome', name='welcome'),
    url(r'^scan/$', 'scan.scan', name='scan'),
    url(r'^services/new-item/$', 'services.new_item', name='services_new_item'),
    

    
)

urlpatterns += staticfiles_urlpatterns()