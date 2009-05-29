from django.utils.translation import ugettext_lazy as _

# Status constants
DRAFTED_STATUS = 1
PUBLISHED_STATUS = 2
REMOVED_STATUS = 3

STATUS_CHOICES = (
    (DRAFTED_STATUS, _(u'drafted')),
    (PUBLISHED_STATUS, _(u'published')),
    (REMOVED_STATUS, _(u'removed')),
)
