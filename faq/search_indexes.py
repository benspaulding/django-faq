from haystack import indexes
from haystack.sites import site

from faq.models import Topic, Question


class FAQIndexBase(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQIndexBase):
    title = indexes.CharField(model_attr='title', indexed=True)

    def get_query_set(self):
        return Topic.published.all()


class QuestionIndex(FAQIndexBase):
    title = indexes.CharField(model_attr='question', indexed=True)

    def get_query_set(self):
        return Question.published.all()


site.register(Topic, TopicIndex)
site.register(Question, QuestionIndex)
