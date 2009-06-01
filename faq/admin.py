from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from faq.actions import draft, publish, remove
from faq.models import Topic, Question
from faq.forms import QuestionForm


class QuestionInline(admin.TabularInline):
    extra = 1
    form = QuestionForm
    model = Question


class FAQAdminBase(admin.ModelAdmin):
    actions = (draft, publish, remove)
    actions_on_top = True
    actions_on_bottom = True
    list_per_page = 50


class TopicAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'description', 'status', 'sites',
                'template_name')}),
    )
    inlines = (QuestionInline, )
    list_display = ('title', 'description', 'status', 'question_count_drafted',
        'question_count_published', 'question_count_removed',
        'question_count_total')
    list_filter = ('status', 'modified', 'created', 'sites')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')

    def question_count_drafted(self, obj):
        """Returns the number of drafted Questions for this topic."""
        return obj.questions.drafted().count()
    question_count_drafted.short_description = _(u'Drafted')

    def question_count_published(self, obj):
        """Returns the number of published Questions for this topic."""
        return obj.questions.published().count()
    question_count_published.short_description = _(u'Published')

    def question_count_removed(self, obj):
        """Returns the number of removed Questions for this topic."""
        return obj.questions.removed().count()
    question_count_removed.short_description = _(u'Removed')

    def question_count_total(self, obj):
        """Returns the total number of Questions for this topic."""
        return obj.questions.count()
    question_count_total.short_description = _(u'Total')


class QuestionAdmin(FAQAdminBase):
    fieldsets = (
        (None, {
            'fields': ('topic', ('question', 'slug'), 'answer', 'status',
                'ordering')}),
    )
    list_display = ('question', 'topic', 'status', 'ordering')
    list_filter = ('status', 'modified', 'created', 'topic')
    prepopulated_fields = {'slug': ('question', )}
    save_as = True
    search_fields = ('question', 'answer')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
