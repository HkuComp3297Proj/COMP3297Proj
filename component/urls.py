from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Text/(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view_text, name='view_component_text'),
    url(r'^Image/(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view_image, name='view_component_image'),
    url(r'^File/(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view_file, name='view_component_File'),
]
