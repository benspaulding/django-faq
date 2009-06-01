from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop, ungettext

from faq.constants import DRAFTED, PUBLISHED, REMOVED, STATUS_CHOICES


def update_status(modeladmin, request, queryset, status):
    """The workhorse function for the admin action functions that follow."""
    # We loop over the objects here rather than use queryset.update() for
    # two reasons:
    #
    #  1. No one should ever be updating zillions of Topics or Questions, so
    #     performance is not an issue.
    #  2. To be tidy, we want to log what the user has done.
    #
    for obj in queryset:
        obj.status = status
        obj.save()
        # Now log what happened.
        # Use ugettext_noop() 'cause this is going straight into the db.
        log_message = ugettext_noop(u'Changed status to \'%s\'.' %
            obj.get_status_display())
        modeladmin.log_change(request, obj, log_message)

    # Send a message to the user telling them what has happened.
    message_dict = {
        'rows_updated': queryset.count(),
        'verbose_name': modeladmin.model._meta.verbose_name,
        'verbose_name_plural': modeladmin.model._meta.verbose_name_plural,
        'verb': dict(STATUS_CHOICES)[status],
    }
    user_message = ungettext(
        u'%(rows_updated)s %(verbose_name)s was successfully %(verb)s.',
        u'%(rows_updated)s  %(verbose_name_plural)s were successfully %(verb)s.',
        message_dict['rows_updated']) % message_dict
    modeladmin.message_user(request, user_message)

    # Return None to display the change list page again and allow the user
    # to reload the page without getting that nasty "Send the form again ..."
    # warning from their browser.
    return None


def draft(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'drafted'."""
    return update_status(modeladmin, request, queryset, DRAFTED)
draft.short_description = _(u'Draft selected %(verbose_name_plural)s')


def publish(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'published'."""
    return update_status(modeladmin, request, queryset, PUBLISHED)
publish.short_description = _(u'Publish selected %(verbose_name_plural)s')


def remove(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'removed'."""
    return update_status(modeladmin, request, queryset, REMOVED)
remove.short_description = _(u'Remove selected %(verbose_name_plural)s')
