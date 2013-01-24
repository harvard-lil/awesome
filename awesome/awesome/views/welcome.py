from django.shortcuts import render_to_response

"""
If it's a simple view, let's put it here
"""

def not_found(request):
    """The application-wide 404 page."""
    return render_to_response('404.html', {'user': request.user})

def welcome(request):
    """The welcome page."""
    return render_to_response('about.html', {'user': request.user})