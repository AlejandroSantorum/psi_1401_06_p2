from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner!<div><a href='/rango/about/'>About</a></div>")

def about(request):
    return HttpResponse("Rango says here is the about page.<div><a href='/rango/'>Index</a></div>")
