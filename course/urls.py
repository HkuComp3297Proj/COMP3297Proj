from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view, name='view_course'),
    url(r'^create_module/(?P<username>[A-Za-z\d_\s]+)', views.create, name='create_module'),
    url(r'^(?P<module>[A-Za-z\d_\s]+)/', include('module.urls')),

]
