============================================================
 Frequently Asked Question (FAQ) management for Django apps
============================================================

This Django_ application provides the ability to create and manage lists of
Frequently Asked Questions (FAQ), organized by topic.

This project is still under development, though several medium-to-large
websites are currently using it in production. The plan is to get a stable
version with a full test suite and documentation out the door in the coming
months.

.. _Django: http://www.djangoproject.com/

TODO’s
------

Below are tasks that need done, features under consideration, and some
reminders for the future.

* Finish writing tests.
* Write general documentation, and specifically,

  * The change of modified date field behavior. (Dropped null=True, now
    has a date upon creation.) Write migration if necessary.
  * Document removal of custom template name field on Topic. (The feature made
    little sense given the various URL/view setups.) Write migration if
    necessary.

* Finalize Django, Haystack, and Whoosh versions in pip requirements/optionals files.
* Bump the version number.
* Roll a release

  * Create git tag
  * Get on Read the Docs
  * Upload to PyPi


Features
~~~~~~~~

* Create a better interface for ordering questions within a topic.
* Consider if/how to add ordering to Topics. (This is complicated because of
  site relations.)


In the future, when dropping Django 1.2 support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Update to class-based generic views
* Move from Question.save() to model validation?
