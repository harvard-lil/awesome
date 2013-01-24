from awesome.models import Branch, Item
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import httplib
import json
import urllib2

"""
Some services. These often times are translators between front end, AJAXy things, and our API/Model.
"""

@csrf_exempt
def new_item(request):
    """Something coming in from our scan page"""
    
    if 'barcode' not in request.POST:
        return HttpResponse(status=400)
    
    barcode = request.POST["barcode"]
        
    # We have the barcode, we need to determine if it's an isbn or an institution barcode or ... 
    
    
    # If we are using the harvard lookup system
    _item_from_hollis('2342344')
    
    


    # get hollis id from presto
    # use hollis id to hit LC. from LC data, populate title, format, etc,
    # if videofilm get poster from RT 
    
    return HttpResponse('respond here with title', status=200)

def _item_from_hollis(barcode):
    
    """
    url = 'http://webservices.lib.harvard.edu/rest/classic/barcode/cite/' + barcode;   
    print url
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        print('HTTPException')
    except Exception:
        import traceback
        print('generic exception: ' + traceback.format_exc())
        
    print response
    
    jsoned_response = json.loads(response)
    print jsoned_response
    hits = jsoned_response['hits']
    """
    
    
     # Let's assume that the above works. I give it a barcode and it gives me a hollis id
    url = 'http://librarycloud.harvard.edu/v1/api/item/?filter=id_inst:008490789';
    req = urllib2.Request(url)
    
    response = None
    
    try: 
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        print('HTTPException')
    except Exception:
        import traceback
        print('generic exception: ' + traceback.format_exc())
        
       
    jsoned_response = json.loads(response)
    
    docs = jsoned_response['docs'][0]
    print docs['title']
    
    branch = Branch.objects.get(id=1)
    item = Item(branch=branch,
                title=docs['title'],
                creator=docs['creator'][0],
                unique_id=docs['id_inst'],
                catalog_id=docs['id_inst'],
                isbn=docs['id_isbn'][0],
                physical_format=docs['format'],)
    
    
    item.save()