from django.conf import settings
from django.template.loader import render_to_string
from awesome.local_settings import *

def analytics(request):
    """
    Returns analytics code.
    """
    if settings.DEBUG:
      return { 'analytics_code': render_to_string("analytics.html", { 'google_analytics_key': GOOGLE['ANALYTICS_KEY'], 'google_analytics_domain': GOOGLE['ANALYTICS_DOMAIN']}) }
    else:
      return { 'analytics_code': ''}