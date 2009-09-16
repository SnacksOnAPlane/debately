import os

from django.conf.urls.defaults import *

urlpatterns = patterns('debately.views',
    (r'^debates/(\d+)$', 'debate'),
    (r'^debates/create/$', 'createDebate'),
    (r'^users/(.*)', 'userpage'),
    (r'^$', 'index'),
)
