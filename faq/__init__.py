# -*- coding: utf-8 -*-

"""
A Frequently Asked Question (FAQ) management application for Django apps.

This Django_ application provides the ability to create and manage lists of
Frequently Asked Questions (FAQ), organized by topic.

This project is still under development, though several medium-to-large
websites are currently using it in production. The plan is to get a stable
version with a full test suite and documentation out the door in the coming
months.

.. _Django: http://www.djangoproject.com/

"""

from django.utils.translation import ugettext_lazy as _


__version__ = '0.8.3'

# Mark the app_label for translation.
_(u'faq')
