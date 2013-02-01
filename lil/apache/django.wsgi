import os
import sys
 
path = '/srv/www/awesome'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/awesome')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'lil.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()