from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from .models import Category, Course, User, Participant, Enrollment, Module
from .forms import Module_form, Text_Component_form, Image_Component_form, File_Component_form, Video_Component_form
from itertools import chain
from operator import attrgetter


def view_module(request, category, course, module, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module) and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        all_component_list = sorted(chain(this_module[0].component_text_set.all(), this_module[0].component_image_set.all(), this_module[0].component_file_set.all(), this_module[0].component_video_set.all()), key=attrgetter('sequence'))
        component_list = ({'name': m.name, 'sequence': m.sequence+1, 'type': m.component_type} for m in all_component_list)
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category': category,
        'category_list': category_list,
        'course': course,
        'module': {'name': this_module[0].name, 'sequence': this_module[0].sequence+1},
        'component_list': component_list,
        'identity': identity,
        'identity_list': identity_list,
        'username': username}
        if identity == "Participant":
            return render(request, 'module/participant_view.html', arguments)
        elif identity == "Instructor":
            return render(request, 'module/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no module called " + module + ".")

def modify_module(request, category, course, module, username):
    identity = "Instructor"
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    opened = this_course[0].opened
    if opened:
        return HttpResponse("Sorry! The course " + course + " has been opened. No modification on modules is forbidden.")
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(this_user)!=0:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = Module_form(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                this_module[0].modify_module(new_name=form['name'].data, sequence=int(form['sequence'].data))
                return redirect('view_course', category=category, course=course, identity=identity, username=username)
            else:
                 return HttpResponse("Sorry! The Form is invalid!")

        # if a GET (or any other method) we'll create a blank form
        else:
            category_list = (c.name for c in Category.objects.all())
            identity_list = this_user[0].get_identity_list()
            identity_list.remove(identity)
            form = Module_form(initial={'name': this_module[0].name, 'sequence': this_module[0].sequence + 1})
            arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'module': {'name': this_module[0].name, 'sequence': this_module[0].sequence+1},
            'identity': identity,
            'identity_list': identity_list,
            'username': username,
            'form': form}
            return render(request, 'module/modify_module.html', arguments)
    else:
        return HttpResponse("Sorry! There is no course called " + course + ".")


def creation_template(request, category, course, module, username, form):
    identity = "Instructor"
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category': category,
        'category_list': category_list,
        'course': course,
        'module': {'name': this_module[0].name, 'sequence': this_module[0].sequence+1},
        'identity': identity,
        'identity_list': identity_list,
        'username': username,
        'form': form,
        'type': component_type}
        return render(request, 'module/create_component.html', arguments)
    else:
        return HttpResponse("Sorry! There is no module called " + course + ".")

def create_text_component(request, category, course, module, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Text_Component_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Module.create_text_component(name=form['name'].data, module=module, sequence=int(form['sequence'].data), text_field=form['text_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)

    # if a GET (or any other method) we'll create a blank form
    else:
        return creation_template(request, category, course, module, username, form = Text_Component_form())

def create_image_component(request, category, course, module, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Image_Component_form(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Module.create_image_component(name=form['name'].data, module=module, sequence=int(form['sequence'].data), image_field=form['image_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        return creation_template(request, category, course, module, username, form = Image_Component_form())

def create_file_component(request, category, course, module, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = File_Component_form(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Module.create_file_component(name=form['name'].data, module=module, sequence=int(form['sequence'].data), file_field=form['file_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        return creation_template(request, category, course, module, username, form = File_Component_form())

def create_video_component(request, category, course, module, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Video_Component_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Module.create_video_component(name=form['name'].data, module=module, sequence=int(form['sequence'].data), url_field=form['url_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        return creation_template(request, category, course, module, username, form = Video_Component_form())
