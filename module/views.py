from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Module

def index(request, category, course, module):
    if len(Module.objects.filter(name=module))!=0:
        return HttpResponse("Hello, this is View module: " + module + " index.")
    else:
        return HttpResponse("Sorry! There is no module called " + module + ".")

def view(request, category, course, module, identity, user_ID):
    return HttpResponse("This is the module " + module + " page for user " + user_ID + " as a " + identity)

def create(request, category, course, module, user_ID):
    return HttpResponse("This is the create component page for user " + user_ID + " in module " + module)
