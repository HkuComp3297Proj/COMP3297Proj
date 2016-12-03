from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from .models import Component_Text, Component_File, Component_Image

@login_required(login_url='/login/')
def view_text(request, category, course, module, component, identity, username):
    if len(Component_Text.objects.filter(name=component))!=0:
        return HttpResponse("This is View text component: " + component + " page for user " + username + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no text component called " + component + ".")


@login_required(login_url='/login/')
def view_file(request, category, course, module, component, identity, username):
    if len(Component_File.objects.filter(name=component))!=0:
        return HttpResponse("This is View file component: " + component + " page for user " + username + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no file component called " + component + ".")

@login_required(login_url='/login/')
def view_image(request, category, course, module, component, identity, username):
    if len(Component_Image.objects.filter(name=component))!=0:
        return HttpResponse("This is View image component: " + component + " page for user " + username + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no image component called " + component + ".")

def view_video(request, category, course, module, component, identity, username):
    if len(Component_Video.objects.filter(name=component))!=0:
        return HttpResponse("This is View video component: " + component + " page for user " + username + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no video component called " + component + ".")
