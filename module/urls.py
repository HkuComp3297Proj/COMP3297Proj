from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<identity>Participant|Instructor)/(?P<username>[A-Za-z\d_\s]+)', views.view, name='view_module'),
    url(r'^create_component/(?P<username>[A-Za-z\d_\s]+)', views.create, name='create_component'),
    url(r'^(?P<component>[A-Za-z\d_\s]+)/', include('component.urls')),

]
