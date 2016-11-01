from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Text/(?P<identity>participant|instructor)/(?P<user_ID>\d+)', views.view_text, name='view_component_text'),
    url(r'^Image/(?P<identity>participant|instructor)/(?P<user_ID>\d+)', views.view_image, name='view_component_image'),
    url(r'^File/(?P<identity>participant|instructor)/(?P<user_ID>\d+)', views.view_file, name='view_component_File'),
]
