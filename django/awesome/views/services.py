import httplib, json, logging, urllib2, re, datetime, os
from StringIO import StringIO
from threading import Thread

from awesome.models import Branch, Item, Organization

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings


from lxml import etree
import twitter


logger = logging.getLogger(__name__)

try:
    from awesome.local_settings import *
except ImportError, e:
    logger.error('Unable to load local_settings.py:', e)

"""
Some services. These often times are translators between front end, AJAXy things, and our API/Model.
"""


def new_item(request):
    """Something coming in from our scan page"""
    
    if not request.user.is_authenticated():
        return HttpResponse(status=401)
    
    if 'barcode' not in request.POST:
        return HttpResponse(status=400)
    
    barcode = request.POST["barcode"]
    branch = request.POST["branch"]
        
    # We have the barcode, we need to determine if it's an isbn or an institution barcode or ... 
    
    
    # If we are using the harvard lookup system
    
    org = Organization.objects.get(user=request.user)
    branch = Branch.objects.get(slug=branch, organization=org)
    
    message_to_return = "No Title"
    
    if org.service_lookup == "worldcat":
        try:
            message_to_return = _item_from_worldcat(barcode, branch)
        except NameError:
            return HttpResponse("Something went wonky", status=500)
        
    if org.service_lookup == "hollis":
        try:
            message_to_return = _item_from_hollis(barcode, branch)
        except NameError:
            return HttpResponse("Something went wonky", status=500)

    
    return HttpResponse(message_to_return, status=200)
    
def learn_how(request):
    """Something coming in from our landing page"""
    
    
    email = request.POST["email"]
        
    #send_mail('Interested in awesome box', 'My library needs more awesome!', email, ['somethign@law.harvard.edu', 'something@law.harvard.edu'], fail_silently=False)
    
    message = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " " + email+ "\n"
    
    with open(settings.PROJECT_ROOT + os.path.sep + "int-emails.txt", "a") as email_file:
        email_file.write(message)
    
    message_to_return = "Mail sent"
    
    return HttpResponse(message_to_return, status=200)

def _item_from_hollis(barcode, branch):
    
    url = 'http://webservices.lib.harvard.edu/rest/classic/barcode/cite/' + barcode;
    
    req = urllib2.Request(url)
    req.add_header("accept", "application/json")
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from Hollis, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from Hollis, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from Hollis, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from Hollis, generic exception: ' + traceback.format_exc())
    
    jsoned_response = json.loads(response)
    
    hollis_id = jsoned_response["rlistFormat"]["hollis"]["hollisId"]
    
    massaged_hollis_id = hollis_id[:9].zfill(9)
    
        
     # Let's assume that the above works. I give it a barcode and it gives me a hollis id
    url = 'http://librarycloud.harvard.edu/v1/api/item/?filter=id_inst:' + massaged_hollis_id;
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from LibraryCloud, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from LibraryCloud, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from LibraryCloud, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from LibraryCloud, generic exception: ' + traceback.format_exc())
        
       
    jsoned_response = json.loads(response)
    
    docs = jsoned_response['docs'][0]
    
    physical_format = 'book'
    if 'video' in docs['format']:
        physical_format = 'videofilm'
        cover_art = _get_rt_movie_poster(docs['title'])
    elif 'sound' in docs['format']:
        physical_format = 'soundrecording'

    
    
    item = Item(branch=branch,
                title=_simple_massage_text(docs['title']),
                creator=_simple_massage_text(docs['creator'][0]),
                unique_id=docs['id_inst'],
                catalog_id=docs['id_inst'],
                isbn=docs['id_isbn'][0],
                physical_format=docs['format'],)
    
    item.save()
    
    current = ThreadedTweet(item)
    current.start()
    
    
    return _simple_massage_text(docs['title'])
    
def _item_from_worldcat(barcode, branch):
    """Given a barcode, get metadata from worldcat"""
    
    url = "http://www.worldcat.org/webservices/catalog/search/sru?query=srw.sn%3D%22" + barcode + "&wskey=" + WORLDCAT["KEY"] + "&servicelevel=full";
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from WorldCat, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from WorldCat, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from WorldCat, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from WorldCat, generic exception: ' + traceback.format_exc())
    
    
    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.parse(StringIO(response), parser)
    
    unique_id= None
    unique_id_list = tree.xpath('//*[@tag="001"]/text()')
    if unique_id_list:
        unique_id = unique_id_list[0]
    else:
        raise NameError('Error getting Data')
    
    title = 'No title'
    title_list = tree.xpath('//*[@tag="245"]/*[@code="a"]/text()')
    if title_list:
        title = unicode(title_list[0])
    
    creator = ''
    creator_list = tree.xpath('//*[@tag="100"]/*[@code="a"]/text()')
    if creator_list:
        creator = unicode(creator_list[0])
        
    massaged_isbn = None
    isbn_list = tree.xpath('//*[@tag="020"]/*[@code="a"]/text()')
    if isbn_list:
        isbn = isbn_list[0]
        massaged_isbn = isbn.split()[0]
    
    cover_art = ''
    
    physical_format = 'book'
    
    formats = tree.xpath('//*[@tag="300"]/*/text()')
            
    if formats:
        for format in formats:
            if 'video' in format:
                physical_format = 'videofilm'
                cover_art = _get_rt_movie_poster(title)
                break
            elif 'sound' in format:
                physical_format = 'soundrecording'
                break
                
    item = Item(branch=branch,
                title=_simple_massage_text(title),
                creator=_simple_massage_text(creator),
                unique_id=unique_id,
                catalog_id=barcode,
                isbn=massaged_isbn,
                physical_format=physical_format,
                cover_art=cover_art,)
    
    
    item.save()
    
    current = ThreadedTweet(item)
    current.start()
    
    return _simple_massage_text(title)

def _get_rt_movie_poster(title):
    """Try to get a poster url from rottent tomatoes"""
    
    url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=" + ROTTEN_TOMATOES['KEY'] + "&q="+ urlquote(title) + "&page_limit=1";
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from Rotten Tomatoes, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from Rotten Tomatoes, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from Rotten Tomatoes, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from Rotten Tomatoes, generic exception: ' + traceback.format_exc())
    
    jsoned_response = json.loads(response)
    poster_url = None
    
    if 'movies' in jsoned_response:
    	if len(jsoned_response['movies']) > 0:
    		poster_url = jsoned_response['movies'][0]['posters']['profile']

    return poster_url
    
class ThreadedTweet(Thread):
   def __init__ (self,item):
      Thread.__init__(self)
      self.item = item
      
   def run(self):
       """ Tweet the item """

       org = self.item.branch.organization

       # Let's check a couple of twitter config items before trying to tweet
       if org.twitter_oauth_token and org.twitter_oauth_secret:

           link_to_item = org.catalog_base_url + self.item.catalog_id

           # Get a short, bit.ly link to our catalog item
           bitly_url = 'http://api.bit.ly/shorten?version=2.0.1&longUrl=' + urlquote(link_to_item) + '&login=' + BITLY['LOGIN'] + '&apiKey=' + BITLY['KEY'] + '&format=json';

           req = urllib2.Request(bitly_url)

           response = None

           try: 
               f = urllib2.urlopen(req)
               response = f.read()
               f.close()
           except urllib2.HTTPError, e:
               logger.warn('Item from Bitly, HTTPError = ' + str(e.code))
           except urllib2.URLError, e:
               logger.warn('Item from Bitly, URLError = ' + str(e.reason))
           except httplib.HTTPException, e:
               logger.warn('Item from Bitly, HTTPException')
           except Exception:
               import traceback
               logger.warn('Item from Bitly, generic exception: ' + traceback.format_exc())

           jsoned_response = json.loads(response)

           short_url = jsoned_response['results'][link_to_item]['shortUrl'];


           #Tweet the item details and the short url

           twitter_message = self.item.title
           if self.item.creator:
               twitter_message = twitter_message + ' by ' + self.item.creator
               
           twitter_message = twitter_message[0:119] + ' ' + short_url

           api = twitter.Api()
           api = twitter.Api(consumer_key = TWITTER['CONSUMER_KEY'],
                                 consumer_secret = TWITTER['CONSUMER_SECRET'],
                                 access_token_key = org.twitter_oauth_token,
                                 access_token_secret = org.twitter_oauth_secret)

           api.PostUpdate(twitter_message)
       
def _simple_massage_text(to_be_massaged):
    if not to_be_massaged:
        return to_be_massaged
    
    return re.sub(r'[^\w^\d^.]*$', r'',to_be_massaged)
    

def unique_id_awesome_count(request, unique_id):
    """
    This is small service that takes in the institution id and produces an awesome count
    for that id.
    
    (At Harvard we offer a feature in the OPAC that allows the user how many
    times something has been awesomed. Here we take the hollis id and return a count)
    """
    
    org = get_object_or_404(Organization, slug=request.META['subdomain'])
    item_count = Item.objects.filter(unique_id=unique_id, branch__organization=org).count()
    
    response = {'count': item_count}
    jsoned_response = json.dumps(response)
    
    return HttpResponse(jsoned_response, mimetype='application/json')