from django.conf.urls.defaults import *

urlpatterns = patterns('debately.views',
    (r'^debates/(\d+)$', 'debate'),
    (r'^users/(.*)', 'userpage'),
    (r'^$', 'index'),
)
