from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^faq/', include('faq.urls')),
)
