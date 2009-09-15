import os

from django.conf import settings
from django.conf.urls.defaults import *

DEBATELY_STATIC_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')

urlpatterns = patterns('debately.views',
    (r'^debates/(\d+)$', 'debate'),
    (r'^users/(.*)', 'userpage'),
    (r'^$', 'index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',    
    # the following is for service static media in the development
    # environ. Should not be used in production 
    # see http://docs.djangoproject.com/en/dev/howto/static-files/
    # for details
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': DEBATELY_STATIC_PATH}),
    )
    
    # user authentication for development/testing
    urlpatterns+= patterns('',
        (r'^login/', 'django.contrib.auth.views.login',
         {'template_name': 'auth/login.html'}),
        (r'^logout/', 'django.contrib.auth.views.logout',
         {'template_name': 'auth/logout.html'}),
    )                       
    

