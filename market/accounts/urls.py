from django.conf.urls import patterns, url
from .                import views

urlpatterns = patterns(
    '',
    url(r"^$", views.details,
        name='details'),
    url(r'^company/create/$', views.company_create,
        name='company-create'),
    url(r'^company/(?P<slug>[\w-]+)-(?P<pk>\d+)/edit/$', views.company_edit,  name='company-edit'),
)