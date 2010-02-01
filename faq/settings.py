from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Status settings.
# It's unlikely that you should need to change these. But if
# you do, here you go.

DRAFTED = getattr(settings, 'FAQ_DRAFTED', 1)
PUBLISHED = getattr(settings, 'FAQ_PUBLISHED', 2)
REMOVED = getattr(settings, 'FAQ_REMOVED', 3)

STATUS_CHOICES = (
    (DRAFTED, _(u'drafted')),
    (PUBLISHED, _(u'published')),
    (REMOVED, _(u'removed')),
)
STATUS_CHOICES = getattr(settings, 'FAQ_STATUS_CHOICES', STATUS_CHOICES)
