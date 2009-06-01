from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list, object_detail

from faq.models import Topic, Question


def topic_list(request):
    """
    A list view of all published FAQ topics.

    Templates:
        :template:`faq/topic_list.html`
    Context:
        topic_list
            A list of all published :model:`faq.Topic` objects that
            relate to the current :model:`sites.Site`.

    """
    return object_list(request, queryset=Topic.published.all(),
        template_object_name='topic')


def topic_detail(request, slug):
    """
    A detail view of an FAQ topic.

    Templates:
        ``<topic_template_name>``
            If the :model:`faq.Topic` object has a ``template_name`` value,
            the system will attempt to load that template.
        :template:`faq/topic_detail.html`
            If there is no ``template_name`` given or the template specified
            does not exist the standard template will be used.
    Context:
        topic
            An :model:`faq.Topic` object.
        question_list
            A list of all published :model:`faq.Question` objects that relate
            to the given :model:`faq.Topic`.

    """
    extra_context = {
        'question_list': Question.published.filter(topic__slug=slug),
    }

    return object_detail(request, queryset=Topic.published.all(),
        extra_context=extra_context, template_object_name='topic',
        template_name_field='template_name', slug=slug)


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    This view simply redirects to a detail page for the :model:`faq.Question`
    object's related :model:`faq.Topic`, with the addition of a fragment
    identifier that links to the given :model:`faq.Question`, e.g.
    ``faq/topic-slug/#question-slug``.

    Note that a 404 will be raised if the :model:`faq.Question` is not
    published (i.e. it is drafted or removed).

    Thus, the templates and context are those used on the
    :view:`faq.views.topic_detail` view.

    """
    get_object_or_404(Question.published.filter(slug=slug,
        topic__slug=topic_slug))
    topic_url = reverse('faq-topic-detail', kwargs={'slug': topic_slug})
    question_fragment = '#%s' % slug

    return redirect(topic_url + question_fragment, permanent=True)
