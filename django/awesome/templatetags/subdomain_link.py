from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from awesome.models import Organization

register = template.Library()

@register.filter
def subdomain_link(user):
    """
        Given a user, return a subdomain link
    """
    awesome_domain = Site.objects.get_current().domain
    org = Organization.objects.get(user=user)
    slug = org.slug
    
    if not settings.DEBUG:
        return 'http://{slug}.{awesome_domain}'.format(slug=slug, awesome_domain=awesome_domain)
    else:
        return 'http://{awesome_domain}'.format(awesome_domain=awesome_domain)