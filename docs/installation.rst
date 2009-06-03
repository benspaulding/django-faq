==============
 Installation
==============

Installing django-faq in your Django application is fairly straight forward.
In short:

1. Have the required software,
2. Install django-faq on the system or place it somewhere on the
   :envvar:`PYTHONPATH`,
3. Add :mod:`faq` to :const:`INSTALLED_APPS`,
4. Include :mod:`faq.urls` in the appropriate URL conf,
5. Run :command:`./manage.py syncdb`.

Requirements
============

* Python 2.4 or greater,
* Django 1.1 beta or greater (:class:`django.db.models.Max` is used in
  :meth:`Question.save`),
* :mod:`django.contrib.sites`

Install the package
===================

.. highlight:: bash

With PIP, which is by far the easiest::

    pip install django-faq

From source by downloading a tarball then running::

    tar xzf django-faq-{x.x}.tar.gz
    cd django-faq-{x.x}
    python setup.py install

From source by cloning the Git repository::

    git clone git://github.com/benspaulding/django-faq.git
    cd django-faq
    python setup.py install

Alternatively, once you have the source you can manually put the :mod:`faq`
package somewhere on your :envvar:`PYTHONPATH`.

Settings, URLs, database
========================

.. highlight:: python

Add :mod:`faq` to :const:`INSTALLED_APPS` in your settings::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        # ... other apps ...
        'faq',
    )

Include :mod:`faq.urls` in :file:`urls.py`::

    urlpatterns = patterns('',
        (r'^admin/', include(admin.site.urls)),
        # ... other urls ...
        (r'^faq/', include('faq.urls')),
    )

.. highlight:: bash

Finally, sync the database::

    ./manage.py syncdb

Congratulations! Django FAQ is now installed.