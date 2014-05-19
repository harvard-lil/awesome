{% load static %}
{% get_static_prefix as STATIC_PREFIX %}

if('{{style}}' !== 'none' && '{{style}}' !== 'default') {
var fileref=document.createElement("link");
fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "text/css");
fileref.setAttribute("href", "http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}css/widget.css");
//fileref.setAttribute("href", "{{ STATIC_PREFIX }}css/widget.css");
document.getElementsByTagName("head")[0].appendChild(fileref);

document.write('<div class="aw-widget">');
document.write('<img src="http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
//document.write('<img src="http://hlslibappdev.law.harvard.edu:8005{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
}
if('{{style}}' === 'default') {
var fileref=document.createElement("link");
fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "text/css");
fileref.setAttribute("href", "http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}css/widget-new.css");
//fileref.setAttribute("href", "{{ STATIC_PREFIX }}css/widget.css");
document.getElementsByTagName("head")[0].appendChild(fileref);

document.write('<div class="aw-widget">');
}
else {
  document.write('<div class="aw-widget-plain">');
}
document.write('<h4 class="aw-widget-title"><a href="http://{{organization.slug}}.{{awesome_domain}}">Awesome at {{organization}}</a></h4>');
document.write('<div class="aw-widget-list">');
{% for item in items %}		
    var catalogQuery = '{{organization.catalog_base_url}}';
    if('{{organization.catalog_query}}' == 'isbn') {
        catalogQuery = '{{organization.catalog_base_url}}{{item.catalog_id}}';
    }
    else if('{{organization.catalog_query}}' == 'title')
        catalogQuery = '{{organization.catalog_base_url}}{{item.title}}';
    else if('{{organization.catalog_query}}' == 'titleauthor')
        catalogQuery = '{{organization.catalog_base_url}}{{item.title}}+{{item.creator}}';
	document.write('<p class="aw-widget-item"><a href="' + catalogQuery + '" target="_blank">{{item.title}}</a> <span class="aw-widget-creator">{{item.creator}}</span></p>');
{% endfor %}
document.write('</div>');
if('{{style}}' === 'default') {
document.write('<img src="http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}images/widget-exclamation.png" class="aw-widget-exclamation" />');
//document.write('<img src="http://hlslibappdev.law.harvard.edu:8005{{ STATIC_PREFIX }}images/widget-exclamation.png" class="aw-widget-arrow" />');
}
document.write('</div>');