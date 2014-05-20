from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(r'^login/$',    views.login,  name='login'),
    url(r'^logout/$',   views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^change_password/$', views.change_password,  name='change_password'),
    #TODO: доделать досылку емайлов
    url(r'^request_email_change/$', views.request_email_change, name='request_email_change'),
)
