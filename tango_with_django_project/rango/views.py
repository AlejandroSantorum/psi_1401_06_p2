from django.shortcuts import render
from rango.models import Category
# from django.http import HttpResponse


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] =  'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage':
                    'This tutorial has been put together by Alex and Rafael'}
    return render(request, 'rango/about.html', context=context_dict)
