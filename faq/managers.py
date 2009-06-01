from django.db import models
from django.conf import settings

from faq.constants import DRAFTED, PUBLISHED, REMOVED


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


class StatusManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def drafted(self):
        """Returns only items with a status of 'drafted'."""
        return self.get_query_set().filter(status=DRAFTED)

    def published(self):
        """Returns only items with a status of 'published'."""
        return self.get_query_set().filter(status=PUBLISHED)

    def removed(self):
        """Returns only items with a status of 'removed'."""
        return self.get_query_set().filter(status=REMOVED)


class OnSiteManager(StatusManager):
    """Custom manager that returns only items related to the current site."""

    def get_query_set(self):
        return super(OnSiteManager, self).get_query_set().filter(
            **_field_lookups(self.model))


class PublishedManager(models.Manager):
    """Custom manager that returns only published, on-site items."""

    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(
            **_field_lookups(self.model, PUBLISHED))
