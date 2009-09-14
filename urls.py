from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'debately.views.index'),
    (r'^debates/(\d+)$', 'debately.views.debate'),
)
