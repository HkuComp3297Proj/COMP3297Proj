from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<identity>participant|instructor)/(?P<user_ID>\d+)', views.view, name='view_category'),
    url(r'^create_course/(?P<user_ID>\d+)', views.create, name='create_course'),
    url(r'^(?P<course>[A-Za-z\d_\s]+)/', include('course.urls')),

]
