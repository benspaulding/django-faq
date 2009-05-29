from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list, object_detail

from faqs.models import Topic, FAQ


def topic_list(request):
    """
    A list view of all published FAQ topics.

    Templates:
        :template:`faqs/topic_list.html`
    Context:
        topic_list
            A list of all published :model:`faqs.Topic` objects that
            relate to the current :model:`sites.Site`.

    """
    return object_list(request, queryset=Topic.published.all(),
        template_object_name='topic')

def topic_detail(request, slug):
    """
    A detail view of an FAQ topic.

    Templates:
        ``<topic_template_name>``
            If the :model:`faqs.Topic` object has a ``template_name`` value,
            the system will attempt to load that template.
        :template:`faqs/topic_detail.html`
            If there is no ``template_name`` given or the template specified
            does not exist the standard template will be used.
    Context:
        topic
            An :model:`faqs.Topic` object.
        faq_list
            A list of all published :model:`faqs.FAQ` objects that relate
            to the given :model:`faqs.Topic`.

    """
    extra_context = {
        'faq_list': FAQ.published.filter(topic__slug__exact=slug),
    }

    return object_detail(request, queryset=Topic.published.all(),
        extra_context=extra_context, template_object_name='topic',
        template_name_field='template_name', slug=slug)

def faq_detail(request, topic_slug, slug):
    """
    A detail view of an FAQ.

    This view simply redirects to a detail page for the :model:`faqs.FAQ`
    object's related :model:`faqs.Topic`, with the addition of a fragment
    identifier that links to the given :model:`faqs.FAQ`, e.g.
    ``faq/topic-slug/#faq-slug``.

    Note that a 404 will be raised if the :model:`faqs.FAQ` is not published
    (i.e. it is drafted or removed).

    Thus, the templates and context are those used on the
    :view:`faqs.views.topic_detail` view.

    """
    get_object_or_404(FAQ.published.filter(slug__exact=slug,
        topic__slug__exact=topic_slug))
    topic_url = reverse('faqs-topic-detail', kwargs={'slug': topic_slug})
    faq_fragment = '#%s' % slug

    return redirect(topic_url + faq_fragment, permanent=True)
