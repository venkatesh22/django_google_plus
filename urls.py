from django.conf.urls.defaults import *

urlpatterns = patterns('django_google_plus.views',
    url(r'^login/$', 'login_begin', name='google-login'),
    url(r'^complete/$', 'login_complete', name='google-complete'),
    url(r'^home/$', 'welcome', name='welcome'),
)
urlpatterns += patterns('',
  (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
