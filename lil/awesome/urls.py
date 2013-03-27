from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


admin.autodiscover()

urlpatterns = patterns('lil.awesome.views',

    # Common Pages
    url(r'^$', 'landing.landing', name='landing'),
    url(r'^scan/$', 'scan.scan', name='scan'),
    url(r'^feed/$', 'feed.feed', name='feed'),
    url(r'^widget/$', 'widget.widget', name='widget'),
    url(r'^control/$', 'control.home', name='control_home'),
    url(r'^control/org/$', 'control.org', name='control_org'),
    url(r'^control/branch/$', 'control.branch', name='control_branch'),
    url(r'^control/branch/edit/$', 'control.branch_edit', name='control_branch_edit'),
    url(r'^control/branch/delete/$', 'control.branch_delete', name='control_branch_delete'),
    url(r'^control/analytics/$', 'control.analytics', name='control_analytics'),
    url(r'^control/widget$', 'control.widget', name='control_widget'),
    url(r'^services/new-item/$', 'services.new_item', name='services_new_item'),
    url(r'^services/learn-how/$', 'services.learn_how', name='services_learn_how'),
    
    # Session/account management
    url(r'^password/change/$', auth_views.password_change, {'template_name': 'registration/password_change_form.html'}, name='auth_password_change'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^register/$', 'user_management.process_register', name='process_register'),
    url(r'^password/change/$', auth_views.password_change, {'template_name': 'registration/password_change_form.html'}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name': 'registration/password_change_done.html'},   name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='auth_password_reset_done'),
)

urlpatterns += staticfiles_urlpatterns()