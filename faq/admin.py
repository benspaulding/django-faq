# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop, ungettext

from faq.settings import DRAFTED, PUBLISHED, REMOVED, STATUS_CHOICES
from faq.models import Topic, Question
from faq.forms import QuestionForm


# Actions.

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
        'count': queryset.count(),
        'object': modeladmin.model._meta.verbose_name,
        'verb': dict(STATUS_CHOICES)[status],
    }
    if not message_dict['count'] == 1:
        message_dict['object'] = modeladmin.model._meta.verbose_name_plural
    user_message = ungettext(
        u'%(count)s %(object)s was successfully %(verb)s.',
        u'%(count)s  %(object)s were successfully %(verb)s.',
        message_dict['count']) % message_dict
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


# Inlines.

class QuestionInline(admin.TabularInline):
    extra = 1
    form = QuestionForm
    model = Question


# Admins.

class FAQAdminBase(admin.ModelAdmin):
    actions = (draft, publish, remove)
    actions_on_top = True
    actions_on_bottom = True
    list_per_page = 50


class TopicAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'status', 'sites')}),
    )
    inlines = (QuestionInline, )
    list_display = ('title', 'description', 'status', 'question_count')
    list_filter = ('status', 'sites', 'modified', 'created')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')

    def question_count(self, obj):
        """Returns the total number of Questions for this topic."""
        return obj.questions.count()
    question_count.short_description = _(u'No. of Questions')


class QuestionAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': ('topic', 'question', 'slug', 'answer', 'status',
                'ordering')}),
    )
    list_display = ('question', 'topic', 'status', 'ordering')
    list_filter = ('status', 'topic', 'modified', 'created')
    prepopulated_fields = {'slug': ('question', )}
    search_fields = ('question', 'answer')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
