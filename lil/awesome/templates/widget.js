{% load static %}
{% get_static_prefix as STATIC_PREFIX %}

var fileref=document.createElement("link");
fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "text/css");
fileref.setAttribute("href", "{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}css/widget.css");
//fileref.setAttribute("href", "{{ STATIC_PREFIX }}css/widget.css");
document.getElementsByTagName("head")[0].appendChild(fileref);

document.write('<div class="aw-widget">');
document.write('<img src="{{organization.slug}}.{{awesome_domain}}{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
//document.write('<img src="{{ STATIC_PREFIX }}images/widget-arrow.png" class="aw-widget-arrow" />');
document.write('<h4 class="aw-widget-title"><a href="{{organization.slug}}.{{awesome_domain}}">Awesome at {{organization}}</a></h4>');
document.write('<div class="aw-widget-list">');
{% for item in items %}		
	document.write('<p class="aw-widget-item"><a href="{{organization.catalog_base_url}}{{item.catalog_id}}" target="_blank">{{item.title}}</a><br><span class="aw-widget-creator">{{item.creator}}</span></p>');
{% endfor %}
document.write('</div></div>');