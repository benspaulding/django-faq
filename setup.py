import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-faq',
    version='0.8.2',
    description='Frequently Asked Question (FAQ) management for Django apps.',
    url='http://github.com/benspaulding/django-faq/',
    author='Ben Spaulding',
    author_email='ben@benspaulding.com',
    license='BSD',
    download_url='http://github.com/benspaulding/django-faq/tarball/v0.8.2',
    long_description = read('README'),
    packages = ['faq', 'faq.urls', 'faq.views'],
    package_data = {'faq': ['locale/*/LC_MESSAGES/*',
                            'templates/faq/*',
                            'templates/search/indexes/faq/*']},
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Internet :: WWW/HTTP :: Site Management'],
)
