from django.conf.urls import url
from . import component_views
from django.conf.urls.static import static
from COMP3297Proj.settings import MEDIA_ROOT
from COMP3297Proj import settings

urlpatterns = [
    url(r'^modify_component/(?P<username>[A-Za-z\d_\s]+)', component_views.modify_component, name='modify_component'),

    url(r'^Text/(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_text, name='view_component_text'),
    url(r'^Text/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_text, name='view_component_text'),
    url(r'^Image/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_image, name='view_component_image'),
    url(r'^Video/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_video, name='view_component_video'),
    url(r'^File/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', component_views.view_file, name='view_component_file'),
]