from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Get the category associated with the slug from the DB
        category = Category.objects.get(slug=category_name_slug)
        # Get the pages given a retrieved category
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage':
                    'This tutorial has been put together by Alex and Rafael'}
    return render(request, 'rango/about.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # We check if we requested the view from a POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)  # Initialise form to values

        if form.is_valid():  # We check if the form is valid
            # Saves the category to the database, returns the object
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)  # Redirect to the index page
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    # Tries to retrieve the category given the slug
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()  # Saves the page to the database

                return redirect(reverse('rango:show_category',
                                kwargs={'category_name_slug':
                                        category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    # If the request is a POST we process the registry
    if request.method == 'POST':
        # Retrieve the data from forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Process the registry of the user
            user = user_form.save()  # Save the user information to the DB
            user.set_password(user.password)  # Hash the password
            user.save()  # Updates it in the DB

            profile = profile_form.save(commit=False)
            profile.user = user

            # If theres an image, we need to put it in the model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()  # Commits the profile instance
            registered = True

        else:
            # Invalid forms, print errors
            print(user_form.errors, profile_form.errors)

    else:
        # If not a POST we return blank forms to render the template
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
