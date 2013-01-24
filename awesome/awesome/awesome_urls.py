from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('awesome.views',

    # Common Pages
    url(r'^$', 'welcome.welcome', name='welcome'),

    
)

urlpatterns += staticfiles_urlpatterns()