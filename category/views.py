from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Category
from user.models import User

def index(request, category):
    if len(Category.objects.filter(name=category))!=0:
        return HttpResponse("Hello, this is View category: " + category + " index.")
    else:
        return HttpResponse("Sorry! There is no category called " + category + ".")

def view(request, category, identity, username):
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        course_list = (c.name for c in this_category[0].course_set.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        if identity == "Participant":
            arguments = {
            'category': category,
            'category_list': category_list,
            'course_list': course_list,
            'identity': identity,
            'identity_list': identity_list,
            'username': username}
            return render(request, 'category/participant_view.html', arguments)
        elif identity == "Instructor":
            arguments = {
            'category': category,
            'category_list': category_list,
            'course_list': course_list,
            'identity': identity,
            'identity_list': identity_list,
            'username': username}
            return render(request, 'category/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no category called " + category + ".")

def create(request, category, username):
    return HttpResponse("This is the create course page for user " + username + " in category " + category)
