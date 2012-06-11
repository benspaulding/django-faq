# -*- coding: utf-8 -*-

import os

from distutils.core import setup


here = os.path.dirname(__file__)

def get_long_desc():
    return open(os.path.join(here, 'README.rst')).read()

# Function borrowed from carljm.
def get_version():
    fh = open(os.path.join(here, "faq", "__init__.py"))
    try:
        for line in fh.readlines():
            if line.startswith("__version__ ="):
                return line.split("=")[1].strip().strip("'")
    finally:
        fh.close()

setup(
    name='django-faq',
    version=get_version(),
    description='Frequently Asked Question (FAQ) management for Django apps.',
    url='https://github.com/benspaulding/django-faq/',
    author='Ben Spaulding',
    author_email='ben@benspaulding.us',
    license='BSD',
    download_url='http://github.com/benspaulding/django-faq/tarball/v%s' % get_version(),
    long_description = get_long_desc(),
    packages = [
        'faq',
        'faq.tests',
        'faq.urls',
        'faq.views',
    ],
    package_data = {
        'faq': [
            'fixtures/*',
            'locale/*/LC_MESSAGES/*',
            'templates/faq/*',
            'templates/search/indexes/faq/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
