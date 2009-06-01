from django.utils.translation import ugettext_lazy as _


# Status constants
DRAFTED = 1
PUBLISHED = 2
REMOVED = 3

STATUS_CHOICES = (
    (DRAFTED, _(u'drafted')),
    (PUBLISHED, _(u'published')),
    (REMOVED, _(u'removed')),
)
