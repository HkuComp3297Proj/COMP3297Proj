from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, User
from .forms import Course_form

def view_category(request, category, identity, username):
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        course_list = (c.name for c in this_category[0].course_set.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category': category,
        'category_list': category_list,
        'course_list': course_list,
        'identity': identity,
        'identity_list': identity_list,
        'username': username}
        if identity == "Participant":
            return render(request, 'category/participant_view.html', arguments)
        elif identity == "Instructor":
            return render(request, 'category/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no category called " + category + ".")

def create_course(request, category, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Course_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Category.create_course(name=form['name'].data, category=category, instructor=username, description=form['description'].data)
            return redirect('view_category', category=category, identity=identity, username=username)

    # if a GET (or any other method) we'll create a blank form
    else:
        this_category = Category.objects.filter(name=category)
        this_user = User.objects.filter(username=username)
        if len(this_category)!=0 and len(this_user)!=0:
            category_list = (c.name for c in Category.objects.all())
            identity_list = this_user[0].get_identity_list()
            identity_list.remove(identity)
            form = Course_form()
            arguments = {
            'category': category,
            'category_list': category_list,
            'identity': identity,
            'identity_list': identity_list,
            'username': username,
            'form': form}
            return render(request, 'category/create_course.html', arguments)
        else:
            return HttpResponse("Sorry! There is no category called " + category + ".")
