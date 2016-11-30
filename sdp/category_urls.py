from django.conf.urls import include, url
from . import category_views

urlpatterns = [
    url(r'^(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', category_views.view_category, name='view_category'),
    url(r'^create_course/(?P<username>[A-Za-z\d_\s]+)', category_views.create_course, name='create_course'), #name of the template 
    url(r'^(?P<course>[A-Za-z\d_\s]+)/', include('sdp.course_urls')),

]
