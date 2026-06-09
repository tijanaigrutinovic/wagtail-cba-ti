from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from core.blocks import CONTENT_BLOCK_DEFINITIONS


class HomePage(Page):
    body = StreamField(
        CONTENT_BLOCK_DEFINITIONS,
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    template = "home/home_page.html"
