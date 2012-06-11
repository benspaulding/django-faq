# -*- coding: utf-8 -*-

from haystack import indexes
from haystack.sites import site

from faq.settings import SEARCH_INDEX
from faq.models import Topic, Question


class FAQIndexBase(SEARCH_INDEX):

    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQIndexBase):

    def get_queryset(self):
        return Topic.objects.published()


class QuestionIndex(FAQIndexBase):

    def get_queryset(self):
        return Question.objects.published()


site.register(Topic, TopicIndex)
site.register(Question, QuestionIndex)
