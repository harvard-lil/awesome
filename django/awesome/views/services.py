import httplib, json, logging, urllib2, re, datetime, os, itertools
from StringIO import StringIO
from threading import Thread

from awesome.models import Branch, Item, Organization, Classification

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.contrib.sites.models import Site

from lxml import etree, objectify
import twitter
import bottlenose
from xml.dom.minidom import parseString


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
    barcode = barcode.replace('-', '')
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

    
#def amazon(request, isbn):
def amazon(isbn):
    """Given an Amazon URL, get title, creator, etc. from imdapi.com
    """

    aws_key = AMZ['KEY']
    aws_secret_key = AMZ['SECRET_KEY']
    aws_associate_tag = AMZ['ASSOCIATE_TAG']
    blob = {}
        
    amazon = bottlenose.Amazon(aws_key, aws_secret_key, aws_associate_tag)
    response = amazon.ItemLookup(ItemId=isbn, ResponseGroup="BrowseNodes", IdType="ISBN", SearchIndex="Books")
    
    xml = parseString(response)
    
    nodes = xml.getElementsByTagName('Children')
    for node in nodes:
        parent = node.parentNode
        parent.removeChild(node)
        
    categories = []              
    for book in xml.getElementsByTagName('Name'):
        category = str(book.firstChild.nodeValue)
        categories.append(category)
    
    taglists = []
    while 'Books' in categories:
        find = categories.index('Books') + 1
        list = categories[:find]
        if 'Products' not in list:
            taglists.append(list)
        for word in list:
            categories.remove(word)

    subjects = []
    #now, we only return the first item from a list which contains 'Subjects'        
    for tagset in taglists:
        while 'Subjects' in tagset:
            tagset.pop(tagset.index('Subjects'))
            tagset.pop(tagset.index('Books'))
            for subject in tagset:
                subjects.append(subject)
            
    if subjects:
        subjects.sort()
        last = subjects[-1]
        for i in range(len(subjects)-2, -1, -1):
            if last == subjects[i]:
                del subjects[i]
            else:
                last = subjects[i]
            
    blob['subjects'] = ':::'.join(subjects)    
    blob['cats'] = taglists
    
    for subject in subjects:
        _insert_amazon_subject(isbn, subject)
        
    #return HttpResponse(json.dumps(subjects), content_type="application/json", status=200)

def _insert_amazon_subject(isbn, subject):
    subjects = Classification.objects.filter(name=subject)[:1]
    
    classification = Classification(name=subject)
    if len(subjects) > 0:
        classification = subjects[0]   
        
    classification.save()
        
    items = Item.objects.filter(isbn=isbn)
    
    for item in items:
        item.classifications.add(classification)


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
    
    url = "http://www.worldcat.org/webservices/catalog/search/sru?query=srw.sn%3D%22" + barcode + "&wskey=" + WORLDCAT["KEY"] + "&servicelevel=full&maximumRecords=1";
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
                cover_art = _get_tmdb_movie_poster(title)
                break
            elif 'sound' in format:
                physical_format = 'soundrecording'
                break
            elif 'audio' in format:
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
    if(massaged_isbn):
        amazon(massaged_isbn)
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
    
def _get_omdb_movie_poster(title):
    """Try to get a poster url from open movie database"""
    
    url = "http://www.omdbapi.com/?t=" + urlquote(title) + "&y=&plot=short&r=json";
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from Open Movie Database, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from Open Movie Database, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from Open Movie Database, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from Open Movie Database, generic exception: ' + traceback.format_exc())
    
    jsoned_response = json.loads(response)
    poster_url = None
    
    if 'Response' in jsoned_response:
    	if jsoned_response['Response'] == 'True':
    		poster_url = jsoned_response['Poster']

    return poster_url
    
def _get_tmdb_movie_poster(title):
    """Try to get a poster url from TMDB"""
    
    url = "http://api.themoviedb.org/3/search/movie?api_key=" + TMDB['KEY'] + "&query=" + urlquote(title);
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        logger.warn('Item from TMDB, HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.warn('Item from TMDB, URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.warn('Item from TMDB, HTTPException')
    except Exception:
        import traceback
        logger.warn('Item from TMDB, generic exception: ' + traceback.format_exc())
    
    jsoned_response = json.loads(response)
    poster_url = None
    
    if 'results' in jsoned_response:
    	if len(jsoned_response['results']) > 0 and jsoned_response['results'][0]['poster_path'] is not None:
    		poster_url = "https://image.tmdb.org/t/p/w150" + jsoned_response['results'][0]['poster_path']

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
       
            if org.catalog_query == 'isbn':
                link_to_item_id = self.item.catalog_id
            elif org.catalog_query == 'title':
                link_to_item_id = self.item.title
            elif org.catalog_query == 'landing':
                link_to_item_id = ''
                
            link_to_item = org.catalog_base_url + link_to_item_id

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
            if org.twitter_show_title:
                if org.twitter_intro:
                    twitter_message = org.twitter_intro + ' ' + self.item.title
                else:
                    twitter_message = self.item.title
                twitter_message = twitter_message.strip()
                if self.item.creator:
                    twitter_message = twitter_message + ' by ' + self.item.creator
            else:
                twitter_message = org.twitter_intro
               
            twitter_message = twitter_message[0:117] + ' ' + short_url

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
    
def isbn_awesome_count(request, isbn):
    """
    This is small service that takes in the isbn and produces an awesome count
    for that id.
    
    (At Harvard we offer a feature in the OPAC that allows the user how many
    times something has been awesomed. Here we take the isbn and return a count)
    """
    org = get_object_or_404(Organization, slug=request.META['subdomain'])
    
    if ":" in isbn:
        item_count = 0
        isbn_list = isbn.split(":")
        for single_isbn in isbn_list:
            item_count = item_count + Item.objects.filter(isbn=single_isbn, branch__organization=org).count()
    else:
        item_count = Item.objects.filter(isbn=isbn, branch__organization=org).count()
    
    response = {'count': item_count}
    jsoned_response = json.dumps(response)
    
    return HttpResponse(jsoned_response, mimetype='application/json')