from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list

from faq.models import Topic, Question


def _fragmentify(model, slug, url=None):
    get_object_or_404(model.objects.published().filter(slug=slug))
    url = url or reverse('faq-topic-list')
    fragment = '#%s' % slug

    return redirect(url + fragment, permanent=True)


def topic_list(request):
    """
    A list view of all published Topics

    Templates:
        :template:`faq/topic_list.html`
    Context:
        topic_list
            A list of all published :model:`faq.Topic` objects that
            relate to the current :model:`sites.Site`.

    """
    return object_list(request, queryset=Topic.objects.published(),
        template_object_name='topic')


def topic_detail(request, slug):
    """
    A detail view of a Topic

    Simply redirects to :view:`faq.views.topic_list` with the addition of
    a fragment identifier that links to the given :model:`faq.Topic`.
    E.g., ``/faq/#topic-slug``.

    """
    return _fragmentify(Topic, slug)


def question_detail(request, topic_slug, slug):
    """
    A detail view of a Question.

    Simply redirects to :view:`faq.views.topic_list` with the addition of
    a fragment identifier that links to the given :model:`faq.Question`.
    E.g. ``/faq/#question-slug``.

    """
    return _fragmentify(Question, slug)
