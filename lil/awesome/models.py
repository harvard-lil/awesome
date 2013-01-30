from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django import forms

class Organization(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=400)
    slug = models.SlugField()
    service_lookup = models.CharField(max_length=100, default="worldcat")
    catalog_base_url = models.URLField(max_length=2000)
    public_link = models.URLField(max_length=2000)
    public_email = models.EmailField(max_length=254)
    about_page_blurb = models.TextField(max_length=4000)
    twitter_username = models.CharField(max_length=10, null=True, blank=True)
    twitter_consumer_key = models.CharField(max_length=200, null=True, blank=True)
    twitter_consumer_secret = models.CharField(max_length=200, null=True, blank=True)
    twitter_oauth_token = models.CharField(max_length=200, null=True, blank=True)
    twitter_oauth_secret = models.CharField(max_length=200, null=True, blank=True)
    bitly_key = models.CharField(max_length=200, null=True, blank=True)
    worldcat_key = models.CharField(max_length=200, null=True, blank=True)
    
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
    
class Item(models.Model):
    branch = models.ForeignKey(Branch)
    title = models.CharField(max_length=400)
    creator = models.CharField(max_length=400)
    unique_id = models.CharField(max_length=100, null=True, blank=True) #usually the institution id or worldcat
    catalog_id = models.CharField(max_length=200, null=True, blank=True) #the ID we use for linking. probably the institution id, isbn, upc 
    isbn = models.CharField(max_length=20, null=True, blank=True) # used to get the cover images
    physical_format = models.CharField(max_length=50, default="book")
    cover_art = models.URLField(max_length=400, null=True, blank=True)
    latest_checkin = models.DateTimeField(auto_now=True)
    number_checkins = models.PositiveIntegerField(default=1)
    
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
    
class UserRegForm(forms.ModelForm):
    """
    stripped down user reg form
    This is mostly a django.contrib.auth.forms.UserCreationForm
    """
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'duplicate_email': "A user with that email address already exists.",
    }
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = "30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only.",
        error_messages = {
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})
    
    email = forms.RegexField(label="Email", required=True, max_length=254,
        regex=r'^[\w.@+-]+$',
        help_text = "Letters, digits and @/./+/-/_ only. 254 characters or fewer.",
        error_messages = {
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})
    
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    
    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        user = super(UserRegForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        exclude = ('user', 'slug', 'service_lookup', )
