{% load static %}
{% get_static_prefix as STATIC_PREFIX %}

if('{{style}}' !== 'none') {
var fileref=document.createElement("link");
fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "text/css");
fileref.setAttribute("href", "http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}css/widget.css");
//fileref.setAttribute("href", "{{ STATIC_PREFIX }}css/widget.css");
document.getElementsByTagName("head")[0].appendChild(fileref);

document.write('<div class="aw-widget">');
document.write('<img src="http://{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
//document.write('<img src="{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
}
else {
  document.write('<div class="aw-widget-plain">');
}
document.write('<h4 class="aw-widget-title"><a href="http://{{organization.slug}}.{{awesome_domain}}">Awesome at {{organization}}</a></h4>');
document.write('<div class="aw-widget-list">');
{% for item in items %}		
    var catalogQuery = '';
    if('{{organization.catalog_query}}' == 'isbn') {
        catalogQuery = '{{organization.catalog_base_url}}{{item.catalog_id}}';
    }
    else if('{{organization.catalog_query}}' == 'title')
        catalogQuery = '{{organization.catalog_base_url}}{{item.title}}';
	document.write('<p class="aw-widget-item"><a href="' + catalogQuery + '" target="_blank">{{item.title}}</a> <span class="aw-widget-creator">{{item.creator}}</span></p>');
{% endfor %}
document.write('</div></div>');