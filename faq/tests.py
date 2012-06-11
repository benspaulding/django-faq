# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.sites.models import Site

from faq.settings import DRAFTED
from faq.models import Topic, Question, OnSiteManager

##
# Test fragmentify, or just view redirects?
# Test _field_lookups, or just Manager?
# Test admin actions?
##

class BaseTestCase(TestCase):
    """"""

    fixtures = ['test_data']

    def setUp(self):
        # Setup some new objects. We want these instead of ones from the test
        # data because we will be testing for the state of something newly
        # created, which the test data does not contain, obviously.
        self.topics = {
            'new': Site.objects.get_current().faq_topics.create(title=u'Test Topic',
                slug=u'test-topic'),
            'drafted': Topic.objects.get(slug='website'),
            'published': Topic.objects.get(slug='shipping'),
            'removed': Topic.objects.get(slug='black-market-items'),
            'off_site': Topic.objects.get(slug='about-us'),
        }

        self. questions = {
            'new1': self.topics['new'].questions.create(question=u'Where am I?',
                answer=u'That is classified.'),
            'new2': self.topics['new'].questions.create(question=u'Who are you?',
                answer=u'I cannot say.'),
            'drafted': Question.objects.get(slug='in-what-color-box-do-you-ship'),
            'published': Question.objects.get(slug='how-much-does-shipping-cost'),
            'removed': Question.objects.get(slug='what-carrier-do-you-use'),
            'off_site': Question.objects.get(slug='are-you-hiring'),
            'pub_topic_draft': Question.objects.get(slug='do-you-have-an-sla'),
            'pub_topic_removed': Question.objects.get(slug='how-do-you-acquire-black-market-items'),
        }


# Model and Manager test cases.

class ManagerTestCase(BaseTestCase):
    """"""

    pass


class ModelsTestCase(BaseTestCase):
    """"""

    def testManager(self):
        # Because of our sublcassing with the models, be certain that the
        # manager is wired up correctly.
        self.assertTrue(isinstance(Topic.objects, OnSiteManager))
        self.assertTrue(isinstance(Question.objects, OnSiteManager))

    def testUnicode(self):
        # Ensure that we don't absent-mindedly change what the `__unicode__()`
        # method returns.
        self.assertEqual(self.topics['new'].__unicode__(),
            self.topics['new'].title)
        self.assertEqual(self.questions['new1'].__unicode__(),
            self.questions['new1'].question)

    def testDefaultStatus(self):
        # Items created without choosing a status should be drafted by default.
        self.assertEqual(self.topics['new'].status, DRAFTED)
        self.assertEqual(self.questions['new1'].status, DRAFTED)

    def testSlugOnSave(self):
        # Be sure we are properly creating slugs for questions that are created
        # without them (those created as an inline to a topic).
        self.assertEqual(self.questions['new1'].slug, u'where-am-i')
        self.assertEqual(self.questions['new2'].slug, u'who-are-you')

    def testOrderingOnSave(self):
        # Be sure we are properly calculating and filling the ordering field
        # when a user leaves it blank.
        self.assertEqual(self.questions['new1'].ordering, 1)
        self.assertEqual(self.questions['new2'].ordering, 2)


# View test case.

class ViewsBaseTestCase(BaseTestCase):
    """"""

    def setUp(self):
        # Call `super` first because we used some of the stuff that it set up.
        super(ViewsBaseTestCase, self).setUp()

        # Set up some responses. We do this here because we are going to be
        # testing on these responses with various methods here and in subclasses.
        self.responses = {
            'topic_list': self.client.get('/'),
            'topic_detail': self.client.get(
                self.topics['published'].get_absolute_url(), follow=True),
            'question_detail': self.client.get(
                self.questions['published'].get_absolute_url(), follow=True),
        }


class ViewsShallowTestCase(ViewsBaseTestCase):

    urls = 'faq.urls.shallow'

    def testTopicDetail(self):
        # Redirects to a fragment identifier on the topic list.
        self.assertRedirects(self.responses['topic_detail'],
            '/#shipping', status_code=301)

    def testQuestionDetail(self):
        # Redirects to a fragment identifier on the topic list.
        self.assertRedirects(self.responses['question_detail'],
            '/#how-much-does-shipping-cost', status_code=301)


class ViewsNormalTestCase(ViewsShallowTestCase):
    """"""

    urls = 'faq.urls.normal'

    def testTopicDetail(self):
        # Does not redirect.
        self.assertEqual(self.responses['topic_detail'].status_code, 200)
        # Check for our extra_context.
        # Must `list()` the QuerySets because querysets are unique.
        self.assertEqual(list(self.responses['topic_detail'].context['question_list']),
            list(self.topics['published'].questions.published()))

    def testQuestionDetail(self):
        # Redirects to a fragment identifier on the topic detail.
        self.assertRedirects(self.responses['question_detail'],
            '/shipping/#how-much-does-shipping-cost', status_code=301)


class ViewsDeepTestCase(ViewsNormalTestCase):
    """"""

    urls = 'faq.urls.deep'

    def testQuestionDetail(self):
        # Does not redirect.
        self.assertEqual(self.responses['question_detail'].status_code, 200)
        # Check for our extra_context.
        self.assertEqual(self.responses['question_detail'].context['topic'],
            self.questions['published'].topic)
