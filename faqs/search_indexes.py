from haystack import indexes
from haystack.sites import site

from faqs.models import Topic, FAQ


class FAQsIndexBase(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)


class TopicIndex(FAQsIndexBase):
    title = indexes.CharField(model_attr='title', indexed=True)

    def get_query_set(self):
        return Topic.published.all()


class FAQIndex(FAQsIndexBase):
    title = indexes.CharField(model_attr='question', indexed=True)

    def get_query_set(self):
        return FAQ.published.all()


site.register(Topic, TopicIndex)
site.register(FAQ, FAQIndex)
