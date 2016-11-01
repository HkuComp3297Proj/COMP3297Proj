from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course

def index(request, category, course):
    if len(Course.objects.filter(name=course))!=0:
        return HttpResponse("Hello, this is View course: " + course + " index.")
    else:
        return HttpResponse("Sorry! There is no course called " + course + ".")

def view(request, category, course, identity, user_ID):
    return HttpResponse("This is the course " + course + " page for user " + user_ID + " as a " + identity)

def create(request, category, course, user_ID):
    return HttpResponse("This is the create module page for user " + user_ID + " in course " + course)
