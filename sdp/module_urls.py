from django.conf.urls import include, url
from . import module_views

urlpatterns = [
<<<<<<< HEAD
    url(r'^(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', module_views.view_module, name='view_module'),
    url(r'^modify_module/(?P<username>[A-Za-z\d_\s]+)', module_views.modify_module, name='modify_module'),
=======
    url(r'^(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', module_views.view_module, name='view_module'),
>>>>>>> 29cd4a54d27828f99fc5e4b7389deb8d543720e4
    url(r'^create_text_component/(?P<username>[A-Za-z\d_\s]+)', module_views.create_text_component, name='create_text_component'),
    url(r'^create_image_component/(?P<username>[A-Za-z\d_\s]+)', module_views.create_image_component, name='create_image_component'),
    url(r'^create_file_component/(?P<username>[A-Za-z\d_\s]+)', module_views.create_file_component, name='create_file_component'),
    url(r'^create_video_component/(?P<username>[A-Za-z\d_\s]+)', module_views.create_video_component, name='create_video_component'),
    url(r'^(?P<component>[A-Za-z\d_\s]+)/', include('sdp.component_urls')),
]
