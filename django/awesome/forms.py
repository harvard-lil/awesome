from awesome.models import Organization, Branch, Shelf

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
        help_text = "Used to sign into your account",
        error_messages = {
            'invalid': "30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."})
    
    email = forms.RegexField(label="Email", required=True, max_length=254,
        regex=r'^[\w.@+-]+$',
        help_text = "So we can contact you about your account",
        error_messages = {
            'invalid': "Letters, digits and @/./+/-/_ only. 254 characters or fewer."})
    
    
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
        widgets = {
          'about_page_blurb': forms.Textarea(attrs={'rows':4}),
        }
        exclude = ('user', 'slug', 'service_lookup', 'twitter_username', 'twitter_oauth_token', 'twitter_oauth_secret', 'twitter_show_title', 'twitter_intro', 'is_active')
        
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['cover_user_id'].help_text = "'client' for Syndetic Solutions, 'userID' for Content Cafe, 'customerid' for TLC"
        self.fields['cover_service'].help_text = "Be sure your terms of service allow use of cover images on this website"
        self.fields['catalog_base_url'].label = "Catalog search URL"
    

class TwitterSettingsForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['twitter_show_title', 'twitter_intro']
    
        
class OrganizationFormRegistration(forms.ModelForm):
            
    class Meta:
        model = Organization
        exclude = ('user', 'twitter_username', 'twitter_oauth_token', 'twitter_oauth_secret', 'twitter_show_title', 'twitter_intro')
        
        
class OrganizationFormSelfRegistration(forms.ModelForm):

    error_messages = {
        'duplicate_slug': "Somebody already claimed that domain.",
    }
            
    class Meta:
        model = Organization
        fields = ("name", "slug", "catalog_base_url", "public_link")
        
    def clean_slug(self):
        # Since slug is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        slug = self.cleaned_data["slug"]
        try:
            Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return slug
        raise forms.ValidationError(self.error_messages['duplicate_slug'])
        
    def __init__(self, *args, **kwargs):
            super(OrganizationFormSelfRegistration, self).__init__(*args, **kwargs)
            self.fields['slug'].label = "Your Awesome Box address"
            self.fields['slug'].help_text = ".awesomebox.io"
            self.fields['name'].label = "Name of your library"
            self.fields['public_link'].label = "Your library website"
            self.fields['catalog_base_url'].label = "Link to your catalog"
            self.fields.keyOrder = [
            'name',
            'public_link',
            'catalog_base_url',
            'slug']
        
        
class BranchForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(BranchForm, self).__init__(*args, **kwargs)
            self.fields['slug'].label = "Web friendly name (letters, numbers, underscores or hyphens)"

    class Meta:
        model = Branch
        exclude = ('organization', )

class AnalyticsForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    

class ShelfForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShelfForm, self).__init__(*args, **kwargs)
        self.fields['slug'].label = "Web friendly name (letters, numbers, underscores or hyphens)"
    
    class Meta:
        model = Shelf
        exclude = ('organization')
        widgets = {
          'description': forms.Textarea(attrs={'rows':4}),
        }
        
    def form_valid(self):
        self.object = self.save(commit=False)
        try:
            self.object.full_clean()
        except ValidationError:
            # here you can return the same view with error messages
            # e.g. field level error or...
            self._errors["slug"] = self.error_class([u"You already have a shelf with that name."])
            return False
        return True
        