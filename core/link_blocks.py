from wagtail import blocks
from wagtail.blocks import PageChooserBlock


class PageOrUrlLinkBlock(blocks.StructBlock):
    page = PageChooserBlock(
        required=False,
        label="Internal page",
        help_text="Choose a page on this site.",
    )
    url = blocks.CharBlock(
        required=False,
        label="URL",
        help_text=(
            "External URL, relative path, or anchor "
            "(e.g. https://example.com, /contact, #faq). "
            "Used when no page is selected."
        ),
    )

    class Meta:
        icon = "link"
        label = "Link"


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    page = PageChooserBlock(
        required=False,
        label="Internal page",
        help_text="Choose a page on this site.",
    )
    url = blocks.CharBlock(
        required=False,
        label="URL",
        help_text=(
            "External URL or relative path. "
            "Used when no page is selected."
        ),
    )

    class Meta:
        icon = "link"
        label = "Link"
