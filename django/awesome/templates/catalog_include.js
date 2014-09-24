{% load static %}
{% get_static_prefix as STATIC_PREFIX %}

if({{item_count}} > 0) {
    document.write('<img id="ab-awesome-indicator" src="http://{{awesome_domain}}{{ STATIC_PREFIX }}images/awesome-yay.png">');
}