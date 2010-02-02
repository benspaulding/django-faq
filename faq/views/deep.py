from django.views.generic.list_detail import object_detail

from faq.models import Topic, Question


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    Templates:
        :template:`faq/question_detail.html`
    Context:
        question
            A :model:`faq.Question`.
        topic
            The :model:`faq.Topic` object related to ``question``.

    """
    extra_context = {
        'topic': Topic.objects.published().get(slug=topic_slug),
    }

    return object_detail(request, queryset=Question.objects.published(),
        extra_context=extra_context, template_object_name='question',
        slug=slug)
