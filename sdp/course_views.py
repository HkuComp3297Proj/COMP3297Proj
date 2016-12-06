from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from .models import Category, Course, User, Participant, Enrollment
from .forms import Module_form
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def view_course(request, category, course, identity, username):
    if request.user.username!=username:
        return HttpResponse("Sorry! You don't have access to this page!")
    else:
        this_category = Category.objects.filter(name=category)
        this_course = this_category[0].course_set.filter(name=course)
        this_user = User.objects.filter(username=username)
        opened = this_course[0].opened
        if len(this_category)!=0 and len(this_course)!=0 and len(this_user)!=0:
            category_list = (c.name for c in Category.objects.all())
            module_list = ({'name': m.name, 'sequence': m.sequence+1} for m in this_course[0].module_set.all().order_by('sequence'))
            identity_list = this_user[0].get_identity_list()
            identity_list.remove(identity)
            arguments = {
            'category': category,
            'category_list': category_list,
            'course': course,
            'open': opened,
            'instructor': this_course[0].instructor.username,
            'description':this_course[0].description,
            'module_list': module_list,
            'identity': identity,
            'identity_list': identity_list,
            'username': username}
            if identity == "Participant":
                if not this_course[0].opened:
                    return HttpResponse("Sorry! There is no course called " + course + ".")
                participant = Participant.objects.filter(username=username)[0]
                arguments['is_enrolled'] = participant.is_enrolled()
                arguments['is_current_enrolled'] = False
                if arguments['is_enrolled']:
                    current_enrollment = participant.enrollment_set.filter(completion_date__isnull=True)[0]
                    if current_enrollment.course.name == course:
                        arguments['is_current_enrolled'] = True
                        arguments['current_progress'] = current_enrollment.module_progress + 1
                enrolled_course = (e.course.name for e in participant.enrollment_set.filter(completion_date__isnull=False))
                arguments['is_past_enrolled'] = False
                for n in enrolled_course:
                    if n == course:
                        arguments['is_past_enrolled'] = True
                        break
                if request.method == 'POST':
                    if (arguments['is_current_enrolled'] or arguments['is_past_enrolled']) and ('drop' in request.POST):
                        participant.drop(course)
                    elif 'enroll' in request.POST:
                        participant.enroll(course)
                    return redirect('view_course', category=category, course=course, identity=identity, username=username)
                else:
                    return render(request, 'course/participant_view.html', arguments)
            elif identity == "Instructor":
                if request.method == 'POST':
                    this_course[0].open()
                    return redirect('view_course', category=category, course=course, identity=identity, username=username)
                else:
                    return render(request, 'course/instructor_view.html', arguments) #Different views for instructor of the course and other instructors
        else:
            return HttpResponse("Sorry! There is no course called " + course + ".")

@login_required(login_url='/login/')
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
            if form['sequence'].data:
                Course.create_module(name=form['name'].data, category=category, course=course, sequence=int(form['sequence'].data))
            else:
                Course.create_module(name=form['name'].data, category=category, course=course, sequence=1000)
            return redirect('view_course', category=category, course=course, identity=identity, username=username)
        else:
            return HttpResponse("Sorry! This is not valid! Please go back!" + str(form.errors))

    # if a GET (or any other method) we'll create a blank form
    else:
        this_category = Category.objects.filter(name=category)
        this_course = this_category[0].course_set.filter(name=course)
        this_user = User.objects.filter(username=username)
        opened = this_course[0].opened
        if opened:
            return HttpResponse("Sorry! The course " + course + " has been opened. No creation on modules is forbidden.")
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
