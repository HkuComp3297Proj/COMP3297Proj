from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from sdp.models import Category, User

def view_index(request, identity, username):
    this_user = User.objects.filter(username=username)
    if len(this_user)!=0:
        return HttpResponse("OKay! " + username + " " + identity)
        category_list = (c.name for c in Category.objects.all())
        identity_list = this_user[0].get_identity_list()
        identity_list.remove(identity)
        arguments = {
        'category_list': category_list,
        'identity': identity,
        'identity_list': identity_list,
        'username': username}
        return render(request, 'index/view.html', arguments)
    else:
        return HttpResponse("Sorry! " + username + " " + identity)
