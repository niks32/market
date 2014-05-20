from django.conf        import settings
from django.conf.urls   import patterns, include, url
from django.contrib     import admin

from .core.urls         import urlpatterns as core_urls
from .registration.urls import urlpatterns as reg_urls
from .accounts.urls     import urlpatterns as account_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',         include(core_urls, namespace='home')),
    url(r'^admin/',   include(admin.site.urls)),
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^profile/', include(reg_urls,     namespace='registration')),
    url(r'^captcha/', include('captcha.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
