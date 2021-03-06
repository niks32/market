from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'category/$', views.category,
        name="category"),
    url(r'^category/(?P<slug>[a-z0-9-]+?)/$', views.category_index,
        name='category'),
    url(r'^(?P<slug>[a-z0-9-]+?)-(?P<product_id>[0-9]+)/$', views.product_details,
        name='details'),

)
