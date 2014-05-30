from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='homepage'),
    url(r'^work/$', views.work, name='work'),
    url(r'^getphonecall$', views.getphonecall, name='getphonecall'),
)
