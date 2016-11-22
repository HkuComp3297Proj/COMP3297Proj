from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from .models import Category, Course, User, Participant, Enrollment, Module
from .forms import Text_Component_form, Image_Component_form, File_Component_form
from itertools import chain
from operator import attrgetter


def view_module(request, category, course, module, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module) and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        all_component_list = sorted(chain(this_module[0].component_text_set.all(), this_module[0].component_image_set.all(), this_module[0].component_file_set.all()), key=attrgetter('sequence'))
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

def creation_template(request, category, course, module, username, component_type):
    identity = "Instructor"
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        form = None
        if component_type == "Text":
            form = Text_Component_form()
        if component_type == "File":
            form = File_Component_form()
        elif component_type == "Image":
            form = Image_Component_form()
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
        return creation_template(request, category, course, module, username, component_type='Text')

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
        return creation_template(request, category, course, module, username, component_type='Image')

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
        return creation_template(request, category, course, module, username, component_type='File')
