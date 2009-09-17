import os

from django.conf.urls.defaults import *

urlpatterns = patterns('debately.views',
    (r'^debates/challenge/(\d+)', 'challenge_debate'),
    (r'^debates/create/$', 'createDebate'),
    (r'^debates/(\d+)$', 'debate'),
    (r'^users/(.*)', 'userpage'),
    (r'^$', 'index'),
)
