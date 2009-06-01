from django.conf.urls.defaults import *

from faq.views import topic_list, topic_detail, question_detail


urlpatterns = patterns('',
    url(r'^$', topic_list, name='faq-topic-list'),
    url(r'^(?P<slug>[-\w]+)/$', topic_detail, name='faq-topic-detail'),
    url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/$', question_detail,
        name='faq-question-detail'),
)
