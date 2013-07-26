import logging

logger = logging.getLogger(__name__)

class SubdomainMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        # thanks to http://thingsilearned.com/2009/01/05/using-subdomains-in-django/
        
        try:
            from awesome.local_settings import *
        except ImportError, e:
            logger.error('Unable to load local_settings.py:', e)
        
        # This is our kludgy third level domain testing logic
        # If out setings say to TEST_HOME, we'll serve up the none-library specific page (awesomebox.io)
        #
        # If we're not testing home, we'll get the domain from the URL (This is what happens in prod for
        # things like somerville.awesomebox.io)
        #
        # If we're testing our third level domain (we're testing somerville.awesomebox.io, but our dev
        # url is localhost:8000), we use the THIRD_LELVEL_DOMAIN setting in our local_settings
        
        if not DEV_SETTINGS['TEST_HOME']:        
            host = request.META.get('HTTP_HOST', '')
            host_s = host.replace('www.', '').split('.')
        
            if len(host_s) > 2:
                request.META['subdomain'] = ''.join(host_s[:-2])
            if DEV_SETTINGS['TEST_THIRD_LEVEL_DOMAIN']:
                request.META['subdomain'] = DEV_SETTINGS['THIRD_LELVEL_DOMAIN']
