from django.conf.urls import patterns, url
from .                import views

urlpatterns = patterns(
    '',
    url(r"^$", views.details,
        name='details'),
    url(r'^company/create/$', views.company_create,
        name='company-create'),
    url(r'^company/(?P<slug>[\w-]+)-(?P<pk>\d+)/edit/$', views.company_edit,
        name='company-edit'),
    url(r'^company/(?P<pk>\d+)/make-default/$', views.company_make_default,
        name='company-make-default'),
    url(r'^company/(?P<slug>[\w-]+)-(?P<pk>\d+)/delete/$', views.company_delete,
        name='company-delete'),
)