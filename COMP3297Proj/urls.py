"""COMP3297Proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import view_index, userlogin,register, userlogout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views
from django_downloadview import ObjectDownloadView
from sdp.models import Component_File

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', userlogin, name='login'),
    url(r'^logout/', userlogout, name='logout'),
    url(r'^register/', register, name='register'),
    url(r'^index/(?P<identity>Participant|Instructor|HR|Administrator)/(?P<username>[A-Za-z\d_\s]+)', view_index, name='view_index'),
    url(r'^(?P<category>[A-Za-z\d_\s]+)/', include('sdp.category_urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

download_views = ObjectDownloadView.as_view(model=Component_File)

urlpatterns += [
        url(r'^media/(?P<path>.*)$', views.serve),
        #url(r'^download_views/(?P<pk>[0-9]+)/$', download_views, name='download' )
    ]
