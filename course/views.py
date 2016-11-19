from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course

def index(request, category, course):
    if len(Course.objects.filter(name=course))!=0:
        return HttpResponse("Hello, this is View course: " + course + " index.")
    else:
        return HttpResponse("Sorry! There is no course called " + course + ".")

def view(request, category, course, identity, username):
    if len(Course.objects.filter(name=course))!=0:
        return HttpResponse("This is the course " + course + " page for user " + username + " as a " + identity)
    else:
        return HttpResponse("Sorry! There is no course called " + course + ".")

def create(request, category, course, username):
    return HttpResponse("This is the create module page for user " + username + " in course " + course)
