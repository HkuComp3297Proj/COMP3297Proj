from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<identity>participant|instructor)/(?P<user_ID>\d+)', views.view, name='view_module'),
    url(r'^create_component/(?P<user_ID>\d+)', views.create, name='create_component'),
    url(r'^(?P<component>[A-Za-z\d_\s]+)/', include('component.urls')),

]
