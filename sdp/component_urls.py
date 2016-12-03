from django.conf.urls import url
from . import component_views

urlpatterns = [
    # url(r'^modify_component/(?P<username>[A-Za-z\d_\s]+)', component_views.modify_component, name='modify_component'),
    url(r'^Text/(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_text, name='view_component_text'),
    url(r'^Text/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_text, name='view_component_text'),
    url(r'^Image/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_image, name='view_component_image'),
    url(r'^File/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_file, name='view_component_file'),
]
