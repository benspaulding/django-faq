import datetime

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from faq.settings import DRAFTED, PUBLISHED, REMOVED, STATUS_CHOICES


# Managers.

def _field_lookups(model, status=None):
    """
    Abstraction of field lookups for managers.

    Returns a dictionary of field lookups for a queryset. The lookups
    will always filter by site. Optionally, if ``status`` is passed to
    the function the objects will also be filtered by the given status.

    This function saves from having to make two different on-site and
    published Managers each for `Topic` and `Question`, and having to move
    Managers out of the `FAQBase` model and into each of the `Topic`
    and `Question` models.

    """
    # Import models here to avoid circular import fail.
    from faq.models import Topic, Question

    field_lookups = {}

    if model == Topic:
        field_lookups['sites__pk'] = settings.SITE_ID

    if model == Question:
        field_lookups['topic__sites__pk'] = settings.SITE_ID
        if status:
            field_lookups['topic__status'] = status

    # Both Topic & Question have a status field.
    if status:
        field_lookups['status'] = status

    return field_lookups


class OnSiteManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def on_site(self):
        """Returns only items related to the current site."""
        return self.get_query_set().filter(**_field_lookups(self.model))

    def drafted(self):
        """Returns only on-site items with a status of 'drafted'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, DRAFTED))

    def published(self):
        """Returns only on-site items with a status of 'published'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, PUBLISHED))

    def removed(self):
        """Returns only on-site items with a status of 'removed'."""
        return self.get_query_set().filter(
            **_field_lookups(self.model, REMOVED))


# Models.

class FAQBase(models.Model):
    """A model holding information common to Topics and Questions."""

    created = models.DateTimeField(_(u'date created'), editable=False)
    modified = models.DateTimeField(_(u'date modified'), editable=False,
        null=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES,
        # TODO: Genericize/fix the help_text.
        db_index=True, default=DRAFTED, help_text=_(u'Only objects with \
            "published" status will be displayed publicly.'))

    objects = OnSiteManager()

    class Meta:
        abstract = True
        get_latest_by = 'modified'

    def save(self):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.modified = datetime.datetime.now()
        super(FAQBase, self).save()


class Topic(FAQBase):
    """A topic that a Question can belong to."""

    title = models.CharField(_(u'title'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the topic. Must be unique.'))
    description = models.TextField(_(u'description'), blank=True,
        help_text=_(u'A short description of this topic.'))
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
        related_name='faq_topics')
    template_name = models.CharField(_(u'template name'), blank=True,
        max_length=255, help_text=_(u'Optional template to use for this \
            topic\'s detail page, e.g., "faq/topics/special.html". If not \
            given the standard template will be used.'))

    class Meta(FAQBase.Meta):
        ordering = ('title', 'slug')
        verbose_name = _(u'topic')
        verbose_name_plural = _(u'topics')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('faq-topic-detail', (), {'slug': self.slug})


class Question(FAQBase):
    """A frequently asked question."""

    question = models.CharField(_(u'question'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the Question. Must be unique.'))
    answer = models.TextField(_(u'answer'))
    topic = models.ForeignKey(Topic, verbose_name=_(u'topic'),
        related_name='questions')
    ordering = models.PositiveSmallIntegerField(_(u'ordering'), blank=True,
        db_index=True, help_text=_(u'An integer used to order the question \
            amongst others related to the same topic. If not given this \
            question will be last in the list.'))

    class Meta(FAQBase.Meta):
        ordering = ('ordering', 'question', 'slug')
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')

    def __unicode__(self):
        return self.question

    def save(self):
        if not self.slug:
            # We populate the slug here because the common case for adding an
            # Question is as an inline to a Topic and InlineModelAdmin does not
            # currently support ``prepopulated_fields`` and it's mean to make
            # the user supply a slug by hand.
            self.slug = slugify(self.question)[:50]
        if not self.ordering:
            # When adding an Question to a Topic, it's easy to overlook the
            # ordering. We don't want to throw an error if it's left blank,
            # so to be nice we'll just put it at the end of the list.
            try:
                # Find the highest ordering value for all other Questions
                # related to the same topic and add 1.
                ordering = self.topic.questions.exclude(pk=self.pk).aggregate(
                    models.Max('ordering'))['ordering__max'] + 1
            except TypeError:
                # There are no other related Questions, so let's set this
                # as no. 1.
                ordering = 1
            self.ordering = ordering
        super(Question, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('faq-question-detail', (), {'topic_slug': self.topic.slug,
            'slug': self.slug})
