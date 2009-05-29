from django import forms

from faqs.models import FAQ


class FAQForm(forms.ModelForm):
    """A form whose only purpose is to manage fields for the FAQInline."""

    class Meta:
        # InlineModelAdmin does not support ``fields``, so if we want to order
        # the fields in an InlineModelAdmin, we must do so with a custom
        # ModelForm. This is not ideal, but at least it gets the job done.
        #
        # Note that ``slug`` is left out of the fields list. This is because
        # we don't show the slug when adding an FAQ as an inline to a topic
        # because InlineModelAdmin does not support ``prepopulated_fields``
        # either, and it's evil to expect the user supply a slug by hand.
        #
        # If the user really wants to edit the slug, they can do so on the
        # FAQ change page.
        fields = ('question', 'answer', 'ordering', 'status')
        model = FAQ
