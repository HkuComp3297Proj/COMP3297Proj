from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view, name='view_category'),
    url(r'^create_course/(?P<username>[A-Za-z\d_\s]+)', views.create, name='create_course'),
    url(r'^(?P<course>[A-Za-z\d_\s]+)/', include('course.urls')),

]
