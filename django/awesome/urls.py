from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from awesome.views.feed import LatestEntriesFeed, BranchLatestEntriesFeed


admin.autodiscover()

urlpatterns = patterns('awesome.views',

    # Common Pages
    url(r'^$', 'landing.landing', name='landing'),
    url(r'^goodbye/$', 'landing.landing_goodbye', name='landing_goodbye'),
    url(r'^explorer/$', 'landing.explorer', name='landing_explorer'),
    url(r'^discover/$', 'landing.discover', name='landing_discover'),
    url(r'^scan/$', 'scan.scan', name='scan'),
    url(r'^feed/$', LatestEntriesFeed()),
    url(r'^feed/(?P<branch_slug>[-\w\d]+)/$', BranchLatestEntriesFeed()),
    url(r'^widget/$', 'widget.widget', name='widget'),
    url(r'^catalog-include/(?P<isbn>[0-9A-Za-z:]+)$', 'widget.catalog_include', name='widget_catalog_include'),
    url(r'^control/$', 'control.home', name='control_home'),
    url(r'^control/org/$', 'control.org', name='control_org'),
    url(r'^control/branch/$', 'control.branch', name='control_branch'),
    url(r'^control/branch/edit/$', 'control.branch_edit', name='control_branch_edit'),
    url(r'^control/branch/delete/$', 'control.branch_delete', name='control_branch_delete'),
    url(r'^control/item/delete/$', 'control.item_delete', name='control_item_delete'),
    url(r'^control/analytics/$', 'control.analytics', name='control_analytics'),
    url(r'^control/supplies$', 'control.supplies', name='control_supplies'),
    url(r'^control/help$', 'control.help', name='control_help'),
    url(r'^control/widget$', 'control.widget', name='control_widget'),
    url(r'^control/twitter/config$', 'control.twitter_config', name='control_twitter_config'),
    url(r'^control/twitter/callback$', 'control.twitter_callback', name='control_twitter_callback'),
    url(r'^control/twitter/settings$', 'control.twitter_settings', name='control_twitter_settings'),
    url(r'^control/export$', 'control.csv_export', name='control_csv_export'),
    url(r'^control/new-shelf/$', 'control.new_shelf', name='control_new_shelf'),
    url(r'^control/shelf-builder/(?P<shelf_slug>[-\w\d]+)/$', 'control.shelf_builder', name='control_shelf_builder'),
    url(r'^services/new-item/$', 'services.new_item', name='services_new_item'),
    url(r'^services/new-shelf-item/$', 'services.new_shelf_item', name='services_new_shelf_item'),
    url(r'^services/new-blank-shelf-item/$', 'services.new_blank_shelf_item', name='services_new_blank_shelf_item'),
    url(r'^services/learn-how/$', 'services.learn_how', name='services_learn_how'),
    url(r'^services/hollis-count/(?P<unique_id>[0-9A-Za-z]+)$', 'services.unique_id_awesome_count', name='services_unique_id_awesome_count'),
    url(r'^services/isbn-count/(?P<isbn>[0-9A-Za-z:]+)$', 'services.isbn_awesome_count', name='services_isbn_awesome_count'),
    url(r'^services/amazon/(?P<isbn>[0-9A-Za-z]+)$', 'services.amazon', name='services_amazon'),
    url(r'^shelf/(?P<shelf_slug>[-\w\d]+)/$', 'landing.shelf', name='landing_shelf'),
    
    # Session/account management
    url(r'^password/change/$', auth_views.password_change, {'template_name': 'registration/password_change_form.html'}, name='auth_password_change'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^register/$', 'user_management.process_register', name='process_register'),
    #url(r'^signup/$', 'user_management.process_self_register', name='process_self_register'),
    url(r'^password/change/$', auth_views.password_change, {'template_name': 'registration/password_change_form.html'}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name': 'registration/password_change_done.html'},   name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='auth_password_reset_done'),
)

urlpatterns += staticfiles_urlpatterns()