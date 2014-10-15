from django.conf        import settings
from django.conf.urls   import patterns, include, url
from django.contrib     import admin

from .core.urls         import urlpatterns as core_urls
from .registration.urls import urlpatterns as reg_urls
from .accounts.urls     import urlpatterns as account_urls
from .product.urls      import urlpatterns as product_urls
from .cart.urls         import urlpatterns as cart_urls
#from .order.urls        import urlpatterns as order_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',         include(core_urls, namespace='home')),
    url(r'^admin/',   include(admin.site.urls)),
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^cart/',    include(cart_urls, namespace='cart')),
    url(r'^profile/', include(reg_urls,     namespace='registration')),
    url(r'^products/',include(product_urls, namespace='product')),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^order/',   include(order_urls, namespace='order')),
    #url(r'',          include('payments.urls')),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))

