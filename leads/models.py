from django.db import models
from django.forms import Textarea

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import FAQBlock


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(AbstractEmailForm):
    template = "leads/contact_page.html"
    landing_page_template = "leads/contact_page_landing.html"

    intro_heading = models.CharField(max_length=255, default="Get in Touch")
    intro_text = models.TextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    faq_section = StreamField(
        [("faq", FAQBlock())],
        use_json_field=True,
        blank=True,
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("faq_section"),
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("from_address"),
                FieldPanel("subject"),
            ],
            heading="Email notifications",
        ),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for field in form.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {css_class}".strip()
            if isinstance(field.widget, Textarea):
                field.widget.attrs.setdefault("rows", 5)
                field.widget.attrs.setdefault(
                    "placeholder",
                    "Tell us about your training needs or questions...",
                )
        return form

    class Meta:
        verbose_name = "Contact Page"
