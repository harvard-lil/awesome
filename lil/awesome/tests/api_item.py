import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.db.models import Count
 
from lil.awesome.models import Organization, Branch, Item, Checkin


class ItemAPITestCase(TestCase):
    """Test the Item API
    """
    
    fixtures = ['smallcompleteset.json']
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_db(self):
        

        
        org = Organization(name='Employee owned dog library',)
        org.save()
        
        orgs = Organization.objects.all()
        #self.assertEqual(len(orgs), 1)
        #print orgs
        
        branch = Branch(organization=orgs[0], name='west branch',)
        branch.save()
        
        branches = Branch.objects.all()
        #self.assertEqual(len(branches), 1)
        #print branches
        
        item = Item(branch=branches[0], title="how to make pants", creator="mr dog", isbn="0224063782", inst_id="009094372", format="book")
        item.save()
        
        items = Item.objects.all()
        #self.assertEqual(len(items), 1)
        #print items
        
        checkin = Checkin(item=item)
        checkin.save()
        
        #checkins = Checkin.objects.all()
        #self.assertEqual(len(checkins), 1)
        #print checkins


        items = Item.objects.filter(branch=branches[0], ).order_by('checkin__checked_in_time')
        #print items.query
        
        print len(items)
        
        for item in items:
            print item
            #print item.checkin_set.all()
        
        #checkins = Checkin.objects.filter()
        
        #print len(checkins)
        
        #for checkin in checkins:
            #print checkin


        most_awesome_list = Item.objects.annotate(num_checkins=Count('checkin')).order_by('-num_checkins')[:5]
        
        for most_awesome in most_awesome_list:
            print most_awesome.title
            print most_awesome.num_checkins
        
# what services do we need to support?
# recently awesome: given a branch, and a media type, return list of items sorted by date
# most awesome: a branch, and a media type, return list of items sorted by most check ins

        
"""
        
class Branch(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=400)
    
    def __unicode__(self):
        return self.name
    
class Item(models.Model):
    branch = models.ForeignKey(Branch)
    title = models.CharField(max_length=400)
    creator = models.CharField(max_length=400)
    isbn = models.CharField(max_length=20)
    inst_id = models.CharField(max_length=20)
    format = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.title
    
class Checkin(models.Model):
    item = models.ForeignKey(Item)
    checked_in_time = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.item.title
"""