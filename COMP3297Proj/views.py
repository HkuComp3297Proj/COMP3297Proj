from django.shortcuts import render, redirect, render_to_response
from .forms import Register_form, Login_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  

# Create your views here.

from django.http import HttpResponse
from sdp.models import Category, User, Course


def view_index(request, identity, username):    #need to handle HR and Administrator as well -- different views? 
    this_user = User.objects.filter(username=username)
    if len(this_user)!=0:
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category_list': category_list,
        'identity': identity,
        'identity_list': identity_list,
        'username': username}
        return render(request, 'index/view.html', arguments) #Need to create a homepage 
    else:
        return HttpResponse("Sorry! " + username + " " + identity)

def register(request):
    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form['username'].data).exists():
                return render_to_response('index/register.html', {"message":"User name already exists!", 'form':form}) #Modify
            else:
                form.save() #Error: no argument 'message' passed 
                return redirect('login')    #Need to add registration success message
        else:
            print (form.errors)
            print (form.non_field_errors)
            return HttpResponse("Errors") #Invalid form (various reason)
    else:
        form = Register_form()
        return render(request, 'index/register.html', {'form':form})


def userlogin(request):
    if request.method == 'POST':
        form = Login_form(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].data,password=form['password'].data)
            if user is not None:
                login(request,user)
                this_user = User.objects.filter(username=form['username'].data)
                identity = form['identity'].data
                category_list = (c.name for c in Category.objects.all())
                identity_list = this_user[0].get_identity_list()
                identity_list.remove(identity)
                arguments = {
                'category_list': category_list,
                'identity': identity,
                'identity_list': identity_list,
                'username': form['username'].data}
                print(form['username'].data + " Login! " + "He is a " + identity)
                #return render(request, 'index/view.html', arguments)

                return redirect('view_index', identity=identity, username=form['username'].data)
                #return HttpResponse(identity)
            else:
                return HttpResponse("Error login message") #Return error login message 
        else:
            print(form.errors)
            print (form.non_field_errors)
            return HttpResponse("Invalid form")
    else:
        form = Login_form()
        return render(request, 'index/login.html', {'form':form})

def userlogout(request):
    logout(request)
    form = Login_form(data=request.POST)
    return redirect('login')



