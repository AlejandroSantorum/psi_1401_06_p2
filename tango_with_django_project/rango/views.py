from django.shortcuts import render
from django.http import HttpResponse

# Django Basics chapter index function
'''
def index(request):
    return HttpResponse("Rango says hey there partner!<div><a href='/rango/about/'>About</a></div>")
'''

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Alejandro and Rafael'}
    return render(request, 'rango/about.html', context=context_dict)
