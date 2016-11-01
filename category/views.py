from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Category

def index(request, category):
    if len(Category.objects.filter(name=category))!=0:
        return HttpResponse("Hello, this is View category: " + category + " index.")
    else:
        return HttpResponse("Sorry! There is no category called " + category + ".")

def view(request, category, identity, user_ID):
    return HttpResponse("This is the category " + category + " page for user " + user_ID + " as a " + identity)

def create(request, category, user_ID):
    return HttpResponse("This is the create course page for user " + user_ID + " in category " + category)
