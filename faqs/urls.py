from django.conf.urls.defaults import *

from faqs.views import topic_list, topic_detail, faq_detail

urlpatterns = patterns('',
    url(r'^$', topic_list, name='faqs-topic-list'),
    url(r'^(?P<slug>[-\w]+)/$', topic_detail, name='faqs-topic-detail'),
    url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', faq_detail,
        name='faqs-faq-detail'),
)
