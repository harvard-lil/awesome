from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib import auth
from awesome.models import UserRegForm

def process_register(request):
    """Register a new user"""
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Create a default shelf for the user
                        
            # Log the user in
            supplied_username = request.POST.get('username', '')
            supplied_password = request.POST.get('password', '')
            user = auth.authenticate(username=supplied_username, password=supplied_password)
            auth.login(request, user)
            
            return HttpResponseRedirect(reverse('landing'))
        else:
            c.update({'form': form})
            return render_to_response('register.html', c)
    else:
        form = UserRegForm()
        c.update({'form': form})
        return render_to_response("register.html", c)