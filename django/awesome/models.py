from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    CATALOG_QUERY_CHOICES = (
        ('isbn', 'ISBN'),
        ('title', 'Title'),
        ('titleauthor', 'Title and Author'),
        ('landing', 'Landing'),
        ('notset', 'Not Set'),
    )
    COVER_QUERY_CHOICES = (
        ('openlibrary', 'Open Library'),
        ('syndetic', 'Syndetic Solutions'),
        ('contentcafe', 'Content Cafe'),
        ('tlc', 'TLC'),
        ('notset', 'Not Set'),
    )
    THEME_QUERY_CHOICES = (
        ('original', 'Original green and blue'),
        ('default', 'Default'),
    )
    user = models.ForeignKey(User)
    name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True)
    service_lookup = models.CharField(max_length=100, default="worldcat")
    catalog_base_url = models.URLField(max_length=2000)
    catalog_query = models.CharField(max_length=100, choices=CATALOG_QUERY_CHOICES, default="isbn")
    cover_service = models.CharField(max_length=100, choices=COVER_QUERY_CHOICES, default="notset")
    cover_user_id = models.CharField(max_length=35, null=True, blank=True)
    cover_password = models.CharField(max_length=35, null=True, blank=True)
    theme = models.CharField(max_length=100, choices=THEME_QUERY_CHOICES, default="default")
    logo_link = models.URLField(max_length=2000, null=True, blank=True)
    about_page_blurb = models.TextField(max_length=4000, default="The Awesome Box is a collaboration with the Harvard Library Innovation Lab. It allows the community to see what others have found helpful, entertaining, or mind-blowing.")
    public_link = models.URLField(max_length=2000, null=True, blank=True)
    public_email = models.EmailField(max_length=254, null=True, blank=True)
    twitter_username = models.CharField(max_length=15, null=True, blank=True)
    twitter_oauth_token = models.CharField(max_length=200, null=True, blank=True)
    twitter_oauth_secret = models.CharField(max_length=200, null=True, blank=True)
    twitter_intro = models.CharField(max_length=35, null=True, blank=True)
    twitter_show_title = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    
    def __unicode__(self):
        return self.name

class Branch(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=400)
    slug = models.SlugField()
    
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
        
class Classification(models.Model):
    name = models.CharField(max_length=400)
    
    def __unicode__(self):
        return self.name
    
class Item(models.Model):
    branch = models.ForeignKey(Branch)
    title = models.CharField(max_length=400)
    creator = models.CharField(max_length=400, null=True, blank=True)
    unique_id = models.CharField(max_length=100, null=True, blank=True) #usually the institution id or worldcat
    catalog_id = models.CharField(max_length=200, null=True, blank=True) #the ID we use for linking. probably the institution id, isbn, upc 
    isbn = models.CharField(max_length=20, null=True, blank=True) # used to get the cover images
    physical_format = models.CharField(max_length=50, default="book")
    cover_art = models.URLField(max_length=400, null=True, blank=True)
    latest_checkin = models.DateTimeField(auto_now=True)
    number_checkins = models.PositiveIntegerField(default=1)
    classifications = models.ManyToManyField(Classification)
    
    def save(self, *args, **kwargs):
        # If we have an item with our unique_id, create a new checkin and update the existing item's latest_checkin and number of checkins
        # else, create a new item and a new checkin

        items = Item.objects.filter(unique_id=self.unique_id, branch=self.branch)[:1]
        
        if len(items) > 0:
            Item.objects.filter(unique_id=self.unique_id, branch=self.branch).update(latest_checkin = datetime.now(), number_checkins=items[0].number_checkins + 1)
            checkin = Checkin(item=items[0])
            checkin.save()
        else:
            super(Item, self).save(*args, **kwargs)
            checkin = Checkin(item=self)
            checkin.save()
        
        
    def __unicode__(self):
        return self.title
    
class Checkin(models.Model):
    item = models.ForeignKey(Item, related_name="checkins")
    checked_in_time = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.item.title