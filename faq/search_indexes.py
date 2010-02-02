from haystack import indexes
from haystack.sites import site

from faq.models import Topic, Question


class FAQIndexBase(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQIndexBase):
    title = indexes.CharField(model_attr='title', indexed=True)

    def get_queryset(self):
        return Topic.objects.published()


class QuestionIndex(FAQIndexBase):
    title = indexes.CharField(model_attr='question', indexed=True)

    def get_queryset(self):
        return Question.objects.published()


site.register(Topic, TopicIndex)
site.register(Question, QuestionIndex)
