from django.db import models
from django.conf import settings

from faqs.constants import DRAFTED, PUBLISHED, REMOVED


def _sites_field_lookups(model):
    """Abstraction of site field lookups for managers."""
    # Import models here to avoid circular import fail.
    from faqs.models import Topic, FAQ

    if model == Topic:
        field_lookup = 'sites__pk'
    elif model == FAQ:
        field_lookup = 'topic__sites__pk'

    return {field_lookup: settings.SITE_ID}


class StatusManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def drafted(self):
        """Returns only items with a status of 'drafted'."""
        return self.get_query_set().filter(status__exact=DRAFTED)

    def published(self):
        """Returns only items with a status of 'published'."""
        return self.get_query_set().filter(status__exact=PUBLISHED)

    def removed(self):
        """Returns only items with a status of 'removed'."""
        return self.get_query_set().filter(status__exact=REMOVED)


class OnSiteManager(StatusManager):
    """Custom manager that returns only items related to the current site."""

    def get_query_set(self):
        return super(OnSiteManager, self).get_query_set().filter(
            **_sites_field_lookups(self.model))


class PublishedManager(models.Manager):
    """Custom manager that returns only published, on-site items."""

    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(
            status__exact=PUBLISHED, **_sites_field_lookups(self.model))
