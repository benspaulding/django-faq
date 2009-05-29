import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from faqs.constants import DRAFTED_STATUS, STATUS_CHOICES
from faqs.managers import StatusManager, OnSiteManager, PublishedManager


class FAQsBase(models.Model):
    """A model holding information common to Topics and FAQs."""

    created = models.DateTimeField(_(u'date created'), editable=False)
    modified = models.DateTimeField(_(u'date modified'), editable=False,
        null=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES,
        # TODO: Genericize/fix the help_text. It applies to both topics & FAQs.
        db_index=True, default=DRAFTED_STATUS, help_text=_(u'Only %(class)s \
            with "published" status will be displayed publicly.'))

    objects = StatusManager()
    on_site = OnSiteManager()
    published = PublishedManager()

    class Meta:
        abstract = True
        get_latest_by = 'modified'

    def save(self):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.modified = datetime.datetime.now()
        super(FAQsBase, self).save()


class Topic(FAQsBase):
    """A topic that an FAQ can belong to."""

    title = models.CharField(_(u'title'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the topic. Must be unique.'))
    description = models.TextField(_(u'description'), blank=True,
        help_text=_(u'A short description of this FAQ topic.'))
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
        related_name='faq_topics')
    template_name = models.CharField(_(u'template name'), blank=True,
        max_length=255, help_text=_(u'Optional template to use for this \
            topic\'s detail page, e.g., "faqs/topics/special.html". If not \
            given the standard template will be used.'))

    class Meta(FAQsBase.Meta):
        ordering = ('title', 'slug')
        verbose_name = _(u'topic')
        verbose_name_plural = _(u'topics')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('faqs-topic-detail', (), {'slug': self.slug})


class FAQ(FAQsBase):
    """A frequently asked question."""

    question = models.CharField(_(u'question'), max_length=255)
    slug = models.SlugField(_(u'slug'), unique=True, help_text=_(u'Used in \
        the URL for the FAQ. Must be unique.'))
    answer = models.TextField(_(u'answer'))
    topic = models.ForeignKey(Topic, verbose_name=_(u'topic'),
        related_name='faqs')
    ordering = models.PositiveSmallIntegerField(_(u'ordering'), blank=True,
        db_index=True, help_text=_(u'An integer used to order the FAQ amongst \
            others related to the same topic. If not given this FAQ will be \
            last in the list.'))

    class Meta(FAQsBase.Meta):
        ordering = ('ordering', 'question', 'slug')
        verbose_name = _(u'FAQ')
        verbose_name_plural = _(u'FAQs')

    def __unicode__(self):
        return self.question

    def save(self):
        if not self.slug:
            # We populate the slug here because the common case for adding an
            # FAQ is as an inline to a topic and InlineModelAdmin does not
            # currently support ``prepopulated_fields`` and it's mean to make
            # the user supply a slug by hand.
            self.slug = slugify(self.question)[:50]
        if not self.ordering:
            # If a user quickly adds an FAQ to a topic, we don't want to throw
            # an error if they left out the ordering (it easy to overlook). To
            # be nice, we'll just put it at the end of the list.
            try:
                # Find the highest ordering value for all other FAQ related to
                # to the same topic and add 1.
                ordering = self.topic.faqs.exclude(pk=self.pk).aggregate(
                    models.Max('ordering'))['ordering__max'] + 1
            except TypeError:
                # There are no other related FAQ, so let's set this as no. 1.
                ordering = 1
            self.ordering = ordering
        super(FAQ, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('faqs-faq-detail', (), {'topic_slug': self.topic.slug,
            'slug': self.slug})
