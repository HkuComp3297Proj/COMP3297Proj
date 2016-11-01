from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Component_Text, Component_File, Component_Image

def view_text(request, category, course, module, component, identity, user_ID):
    if len(Component_Text.objects.filter(name=component))!=0:
        return HttpResponse("This is View text component: " + component + " page for user " + user_ID + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no text component called " + component + ".")

def view_file(request, category, course, module, component, identity, user_ID):
    if len(Component_File.objects.filter(name=component))!=0:
        return HttpResponse("This is View file component: " + component + " page for user " + user_ID + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no file component called " + component + ".")

def view_image(request, category, course, module, component, identity, user_ID):
    if len(Component_Image.objects.filter(name=component))!=0:
        return HttpResponse("This is View image component: " + component + " page for user " + user_ID + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no image component called " + component + ".")
