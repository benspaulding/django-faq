from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from faqs.actions import draft, publish, remove
from faqs.models import Topic, FAQ
from faqs.forms import FAQForm


class FAQInline(admin.TabularInline):
    extra = 1
    form = FAQForm
    model = FAQ


class FAQsAdminBase(admin.ModelAdmin):
    actions = (draft, publish, remove)
    actions_on_top = True
    actions_on_bottom = True
    list_per_page = 50


class TopicAdmin(FAQsAdminBase):
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'description', 'status', 'sites',
                'template_name')
        }),
    )
    inlines = (FAQInline,)
    list_display = ('title', 'description', 'status', 'faq_count_drafted',
        'faq_count_published', 'faq_count_removed', 'faq_count_total')
    list_filter = ('status', 'modified', 'created', 'sites')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')

    def faq_count_drafted(self, obj):
        """Returns the number of drafted FAQ for this topic."""
        return obj.faqs.drafted().count()
    faq_count_drafted.short_description = _(u'Drafted')

    def faq_count_published(self, obj):
        """Returns the number of published FAQ for this topic."""
        return obj.faqs.published().count()
    faq_count_published.short_description = _(u'Published')

    def faq_count_removed(self, obj):
        """Returns the number of removed FAQ for this topic."""
        return obj.faqs.removed().count()
    faq_count_removed.short_description = _(u'Removed')

    def faq_count_total(self, obj):
        """Returns the total number of FAQ for this topic."""
        return obj.faqs.count()
    faq_count_total.short_description = _(u'Total')


class FAQAdmin(FAQsAdminBase):
    fieldsets = (
        (None, {
            'fields': ('topic', ('question', 'slug'), 'answer', 'status',
                'ordering')
        }),
    )
    list_display = ('question', 'topic', 'status', 'ordering')
    list_filter = ('status', 'modified', 'created', 'topic')
    prepopulated_fields = {'slug': ('question',)}
    save_as = True
    search_fields = ('question', 'answer')


admin.site.register(Topic, TopicAdmin)
admin.site.register(FAQ, FAQAdmin)
