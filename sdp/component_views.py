from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Course, User, Participant, Enrollment, Module, Component_Text, Component_Image, Component_File, Component_Video
from .forms import Module_form, Text_Component_form, Image_Component_form, File_Component_form, Video_Component_form
from itertools import chain
from operator import attrgetter

def check_access (course, module, component, username):
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_user = User.objects.filter(username=username)
    if not this_course[0].opened:
        return False
    participant = Participant.objects.filter(username=username)[0]
    is_enrolled = participant.is_enrolled()
    is_current_enrolled = False
    if is_enrolled:
        current_enrollment = participant.enrollment_set.filter(completion_date__isnull=True)[0]
        if current_enrollment.course.name == course:
            is_current_enrolled = True
            current_progress = current_enrollment.module_progress + 1
    enrolled_course = (e.course.name for e in participant.enrollment_set.filter(completion_date__isnull=False))
    is_past_enrolled = False
    for n in enrolled_course:
        if n == course:
            is_past_enrolled = True
            break
    if (not (is_past_enrolled or is_current_enrolled)) or (is_current_enrolled and this_module[0].sequence + 1 > current_progress):
        return False
    return True


@login_required(login_url='/login/')
def view_text(request, category, course, module, component, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_user = User.objects.filter(username=username)
    this_component = Component_Text.objects.filter(name=component)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(component)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'module': module,
            'component': {'name': this_component[0], 'sequence': this_component[0].sequence+1, 'text':this_component[0].text_field, 'type':this_component[0].component_type},
            'identity': identity,
            'identity_list': identity_list,
            'username': username
        }
        if identity == "Participant":
            if check_access(course, module, component, username):
                return render(request, 'component/participant_view.html', arguments)
            else:
                return HttpResponse("Sorry! You are not allowed to view this Component.")
        elif identity == "Instructor":
            return render(request, 'component/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no component called " + component + ".")


@login_required(login_url='/login/')
def view_file(request, category, course, module, component, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_component = Component_File.objects.filter(name=component)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(this_component)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'module': module,
            'component': {'name': this_component[0], 'sequence': this_component[0].sequence+1, 'file':this_component[0].file_field, 'type':this_component[0].component_type},
            'identity': identity,
            'identity_list': identity_list,
            'username': username,
        }
        #return redirect('download', pk=this_component[0].pk)
        if identity == "Participant":
            if check_access(course, module, component, username):
                return render(request, 'component/participant_view.html', arguments)
            else:
                return HttpResponse("Sorry! You are not allowed to view this Component.")
        elif identity == "Instructor":
            return render(request, 'component/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no component called " + component + ".")

@login_required(login_url='/login/')
def view_image(request, category, course, module, component, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_component = Component_Image.objects.filter(name=component)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(this_component)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'module': module,
            'component': {'name': this_component[0], 'sequence': this_component[0].sequence+1, 'image':this_component[0].image_field, 'type':this_component[0].component_type},
            'identity': identity,
            'identity_list': identity_list,
            'username': username
            }
        if identity == "Participant":
            if check_access(course, module, component, username):
                return render(request, 'component/participant_view.html', arguments)
            else:
                return HttpResponse("Sorry! You are not allowed to view this Component.")
        elif identity == "Instructor":
            return render(request, 'component/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no component called " + component + ".")

@login_required(login_url='/login/')
def view_video(request, category, course, module, component, identity, username):
    this_category = Category.objects.filter(name=category)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_component = Component_Video.objects.filter(name=component)
    this_user = User.objects.filter(username=username)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(this_component)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'module': module,
            'component': {'name': this_component[0], 'sequence': this_component[0].sequence+1, 'video':this_component[0].url_field, 'type':this_component[0].component_type},
            'identity': identity,
            'identity_list': identity_list,
            'username': username
        }
        if identity == "Participant":
            if check_access(course, module, component, username):
                return render(request, 'component/participant_view.html', arguments)
            else:
                return HttpResponse("Sorry! You are not allowed to view this Component.")
        elif identity == "Instructor":
            return render(request, 'component/instructor_view.html', arguments)
    else:
        return HttpResponse("Sorry! There is no component called " + component + ".")

@login_required(login_url='/login/')
def modification_template(request, category, course, module, username, component, component_type, form):
    identity = "Instructor"
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    this_course = Course.objects.filter(name=course)
    this_module = Module.objects.filter(name=module)
    this_component = []
    if component_type == "Text":
        this_component = Component_Text.objects.filter(name=component)
    elif component_type == "Image":
        this_component = Component_Image.objects.filter(name=component)
    elif component_type == "File":
        this_component = Component_File.objects.filter(name=component)
    elif component_type == "Video":
        this_component = Component_Video.objects.filter(name=component)
    if this_user[0].username != this_course[0].instructor.username:
        return HttpResponse("Sorry! You do not have the access!")
    if len(this_category)!=0 and len(this_course)!=0 and len(this_module)!=0 and len(this_component)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category': category,
        'category_list': category_list,
        'course': course,
        'module': {'name': this_module[0].name, 'sequence': this_module[0].sequence+1},
        'component':{'name': this_component[0].name, 'sequence': this_component[0].sequence+1},
        'identity': identity,
        'identity_list': identity_list,
        'username': username,
        'form': form,
        'type': component_type}
        return render(request, 'component/modify_component.html', arguments)
    else:
        return HttpResponse("Sorry! There is no component called " + component + ".")

@login_required(login_url='/login/')
def modify_text_component(request, category, course, module, component, username):
    identity = "Instructor"
    this_component = Component_Text.objects.filter(name=component)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Text_Component_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            this_component[0].modify_component(new_name=form['name'].data, sequence=int(form['sequence'].data), text_field=form['text_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Text_Component_form(initial={'name': this_component[0].name, 'sequence': this_component[0].sequence + 1, 'text_field': this_component[0].text_field})
        return modification_template(request, category, course, module, username, component, component_type='Text', form = form)

@login_required(login_url='/login/')
def modify_image_component(request, category, course, module, component, username):
    identity = "Instructor"
    this_component = Component_Image.objects.filter(name=component)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Image_Component_form(request.POST, request.FILES)
        img_to_set = form['image_field'].data
        if img_to_set is None:
            img_to_set = this_component[0].image_field;
        # check whether it's valid:
        if form['name'].data is not None and form['sequence'].data is not None:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            this_component[0].modify_component(new_name=form['name'].data, sequence=int(form['sequence'].data), image_field=img_to_set)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Image_Component_form(initial={'name': this_component[0].name, 'sequence': this_component[0].sequence + 1, 'image_field': this_component[0].image_field})
        return modification_template(request, category, course, module, username, component, component_type='Image', form = form)

@login_required(login_url='/login/')
def modify_file_component(request, category, course, module, component, username):
    identity = "Instructor"
    this_component = Component_File.objects.filter(name=component)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = File_Component_form(request.POST, request.FILES)
        # check whether it's valid:
        if form['name'].data is not None and form['sequence'].data is not None:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            this_component[0].modify_component(new_name=form['name'].data, sequence=int(form['sequence'].data), file_field=form['file_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = File_Component_form(initial={'name': this_component[0].name, 'sequence': this_component[0].sequence + 1, 'file_field': this_component[0].file_field})
        return modification_template(request, category, course, module, username, component, component_type='File', form = form)

@login_required(login_url='/login/')
def modify_video_component(request, category, course, module, component, username):
    identity = "Instructor"
    this_component = Component_Video.objects.filter(name=component)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Video_Component_form(request.POST)
        # check whether it's valid:
        if form['name'].data is not None and form['sequence'].data is not None:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            this_component[0].modify_component(new_name=form['name'].data, module=module, sequence=int(form['sequence'].data), url_field=form['url_field'].data)
            return redirect('view_module', category=category, course=course, module=module, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Video_Component_form(initial={'name': this_component[0].name, 'sequence': this_component[0].sequence + 1, 'url_field': this_component[0].url_field})
        return modification_template(request, category, course, module, username, component, component_type='Video', form = form)

@login_required(login_url='/login/')
def modify_component(request, category, course, module, component, username):
    if len(Component_Text.objects.filter(name=component)) != 0:
        return modify_text_component(request, category, course, module, component, username)
    elif len(Component_Image.objects.filter(name=component)) != 0:
        return modify_image_component(request, category, course, module, component, username)
    elif len(Component_File.objects.filter(name=component)) != 0:
        return modify_file_component(request, category, course, module, component, username)
    elif len(Component_Video.objects.filter(name=component)) != 0:
        return modify_video_component(request, category, course, module, component, username)
    else:
        return HttpResponse("Sorry! No such Component")
