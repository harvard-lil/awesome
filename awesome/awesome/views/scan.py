from django.shortcuts import render_to_response

"""
If it's a simple view, let's put it here
"""

def scan(request):
    """Our scan page"""
    return render_to_response('scan.html', {'user': request.user})
