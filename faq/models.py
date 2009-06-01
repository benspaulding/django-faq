import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from faq.constants import DRAFTED, STATUS_CHOICES
from faq.managers import StatusManager, OnSiteManager, PublishedManager


class FAQBase(models.Model):
    """A model holding information common to Topics and Questions."""

    created = models.DateTimeField(_(u'date created'), editable=False)
    modified = models.DateTimeField(_(u'date modified'), editable=False,
        null=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES,
        # TODO: Genericize/fix the help_text.
        db_index=True, default=DRAFTED, help_text=_(u'Only %(class)s \
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
