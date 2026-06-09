from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, StructBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import CONTENT_BLOCK_DEFINITIONS


class FlexPage(Page):
    body = StreamField(
        CONTENT_BLOCK_DEFINITIONS,
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage", "wagtailcore.Page"]
    template = "content/flex_page.html"

    class Meta:
        verbose_name = "Flexible Page"


class LegalPage(Page):
    intro = models.TextField(blank=True)
    compliance_badges = StreamField(
        [
            (
                "badge",
                StructBlock([
                    ("label", CharBlock()),
                    ("description", CharBlock(required=False)),
                ]),
            ),
        ],
        use_json_field=True,
        blank=True,
    )
    last_updated = models.DateField(null=True, blank=True)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("compliance_badges"),
        FieldPanel("last_updated"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage", "wagtailcore.Page"]
    template = "content/legal_page.html"

    class Meta:
        verbose_name = "Legal Page"
