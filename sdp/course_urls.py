from django.conf.urls import include, url
from . import course_views

urlpatterns = [
    url(r'^(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', course_views.view_course, name='view_course'),
    url(r'^create_module/(?P<username>[A-Za-z\d_\s]+)', course_views.create_module, name='create_module'),
    url(r'^(?P<module>[A-Za-z\d_\s]+)/', include('sdp.module_urls')),

]
