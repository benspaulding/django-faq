# -*- coding: utf-8 -*-

"""
Haystack SearchIndexes for FAQ objects.

Note that these are compatible with both Haystack 1.0 and Haystack 2.0-beta.

The super class for these indexes can be customized by using the
``FAQ_SEARCH_INDEX`` setting.

"""

from haystack import indexes

from faq.settings import SEARCH_INDEX
from faq.models import Topic, Question


# Haystack 2.0 (commit 070d46d72f92) requires that concrete SearchIndex classes
# use the indexes.Indexable mixin. Here we workaround that so our SearchIndex
# classes also work for Haystack 1.X.
try:
    mixin = indexes.Indexable
except AttributeError:
    mixin = object


class FAQIndexBase(SEARCH_INDEX):

    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQIndexBase, mixin):

    # Required method for Haystack 2.0, but harmless on 1.X.
    def get_model(self):
        return Topic

    # ``get_queryset`` is deprecated in Haystack v2, and ``index_queryset``
    # ought to be used instead. But we must use the former to support
    # Haystack < 1.2.4. Support for such older version is likely to be dropped
    # in the near future.
    def get_queryset(self):
        return Topic.objects.published()


class QuestionIndex(FAQIndexBase, mixin):

    # Required method for Haystack 2.0, but harmless on 1.X.
    def get_model(self):
        return Question

    # ``get_queryset`` is deprecated in Haystack v2, and ``index_queryset``
    # ought to be used instead. But we must use the former to support
    # Haystack < 1.2.4. Support for such older version is likely to be dropped
    # in the near future.
    def get_queryset(self):
        return Question.objects.published()


# try/except in order to register search indexes with site for Haystack 1.X
# without throwing exceptions with Haystack 2.0.
try:
    from haystack.sites import site
    site.register(Topic, TopicIndex)
    site.register(Question, QuestionIndex)
except ImportError:
    pass
