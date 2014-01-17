from django.conf.urls.defaults import *

urlpatterns = patterns('django_google_plus.views',
    url(r'^login/$', 'login_begin', name='openid-login'),
    url(r'^complete/$', 'login_complete', name='openid-complete'),
    url(r'^logo.gif$', 'logo', name='openid-logo'),
)
