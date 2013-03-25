import logging

logger = logging.getLogger(__name__)

class SubdomainMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        # thanks to http://thingsilearned.com/2009/01/05/using-subdomains-in-django/
        
        try:
            from lil.awesome.local_settings import *
        except ImportError, e:
            logger.error('Unable to load local_settings.py:', e)
        
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        if len(host_s) > 2:
            request.META['subdomain'] = ''.join(host_s[:-2])
        if DEV_SETTINGS['TEST_THIRD_LEVEL_DOMAIN']:
            request.META['subdomain'] = DEV_SETTINGS['THIRD_LELVEL_DOMAIN']