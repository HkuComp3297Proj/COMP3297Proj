from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from .models import Category, Course, User, Participant, Enrollment
from .forms import Module_form

def view_course(request, category, course, identity, username):
    this_category = Category.objects.filter(name=category)
    this_user = User.objects.filter(username=username)
    this_course = Course.objects.filter(name=course)
    if len(this_category)!=0 and len(this_course)!=0 and len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        module_list = ({'name': m.name, 'sequence': m.sequence+1} for m in this_course[0].module_set.all().order_by('sequence'))
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category': category,
        'category_list': category_list,
        'course': course,
        'instructor':this_course[0].instructor.username,
        'module_list': module_list,
        'identity': identity,
        'identity_list': identity_list,
        'username': username}
        if identity == "Participant":
            participant = Participant.objects.filter(username=username)[0]
            arguments['is_enrolled'] = participant.is_enrolled()
            if arguments['is_enrolled']:
                arguments['enrolled_course'] = participant.enrollment_set.filter(completion_date__isnull=True)[0].course.name
            else:
                arguments['instructor'] = this_course[0].instructor.username
                arguments['description'] = this_course[0].description
            if request.method == 'POST':
                if arguments['is_enrolled']:
                    participant.drop(course)
                else:
                    participant.enroll(course)
                return redirect('view_course', category=category, course=course, identity=identity, username=username)
            else:
                return render(request, 'course/participant_view.html', arguments)
        elif identity == "Instructor":
            return render(request, 'course/instructor_view.html', arguments) #Different views for instructor of the course and other instructors 
    else:
        return HttpResponse("Sorry! There is no course called " + course + ".")

def create_module(request, category, course, username):
    identity = "Instructor"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Module_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Course.create_module(name=form['name'].data, course=course, sequence=int(form['sequence'].data))
            return redirect('view_course', category=category, course=course, identity=identity, username=username)

    # if a GET (or any other method) we'll create a blank form
    else:
        this_category = Category.objects.filter(name=category)
        this_user = User.objects.filter(username=username)
        this_course = Course.objects.filter(name=course)
        if len(this_category)!=0 and len(this_course)!=0 and len(this_user)!=0:
            category_list = (c.name for c in Category.objects.all())
            identity_list = this_user[0].get_identity_list()
            identity_list.remove(identity)
            form = Module_form()
            arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'identity': identity,
            'identity_list': identity_list,
            'username': username,
            'form': form}
            return render(request, 'course/create_module.html', arguments)
        else:
            return HttpResponse("Sorry! There is no course called " + course + ".")
