from wagtail import blocks
from wagtail.blocks import RichTextBlock as WagtailRichTextBlock
from wagtail.images.blocks import ImageChooserBlock

from core.link_blocks import PageOrUrlLinkBlock


class RichTextBlock(WagtailRichTextBlock):
    class Meta:
        icon = "doc-full"
        label = "Text"
        template = "blocks/richtext_block.html"


class HeroBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    subheading = blocks.TextBlock()
    primary_button_text = blocks.CharBlock()
    primary_button_link = PageOrUrlLinkBlock()
    secondary_button_text = blocks.CharBlock(required=False)
    secondary_button_link = PageOrUrlLinkBlock(required=False)
    background_image = ImageChooserBlock(
        required=False,
        help_text="Upload the hero background image.",
    )
    background_image_alt = blocks.CharBlock(
        required=False,
        default="Hero background",
    )

    class Meta:
        icon = "image"
        label = "Hero Section"
        template = "blocks/hero_block.html"


class TabItemBlock(blocks.StructBlock):
    tab_label = blocks.CharBlock()
    heading = blocks.CharBlock()
    body = blocks.TextBlock()
    button_text = blocks.CharBlock(required=False)
    button_link = PageOrUrlLinkBlock(required=False)
    image = ImageChooserBlock(
        required=False,
        help_text="Upload the tab illustration.",
    )
    image_alt = blocks.CharBlock(
        required=False,
        help_text="Describe the image for accessibility.",
    )

    class Meta:
        icon = "doc-full"
        label = "Tab"


class TabsBlock(blocks.StructBlock):
    section_heading = blocks.CharBlock(required=False)
    section_subheading = blocks.TextBlock(required=False)
    section_id = blocks.CharBlock(required=False, default="programs")
    tabs = blocks.ListBlock(TabItemBlock())

    class Meta:
        icon = "list-ol"
        label = "Tabs"
        template = "blocks/tabs_block.html"


class FeatureBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=False,
        help_text="Upload the section image.",
    )
    image_position = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("right", "Right")],
        default="left",
    )
    heading = blocks.CharBlock()
    subheading = blocks.TextBlock(required=False)
    body = RichTextBlock()
    outcomes_heading = blocks.CharBlock(required=False, default="What you'll achieve")
    outcomes = blocks.ListBlock(blocks.CharBlock(), required=False)
    button_text = blocks.CharBlock(required=False)
    button_link = PageOrUrlLinkBlock(required=False)

    class Meta:
        icon = "pick"
        label = "Feature Section"
        template = "blocks/feature_block.html"


class CardItemBlock(blocks.StructBlock):
    icon = ImageChooserBlock(
        required=False,
        help_text="Optional card icon.",
    )
    heading = blocks.CharBlock()
    body = blocks.TextBlock()
    link_text = blocks.CharBlock(required=False)
    link = PageOrUrlLinkBlock(required=False)
    link_meta = blocks.CharBlock(
        required=False,
        help_text="e.g. accet.org — shown on accreditation cards",
    )
    external_link = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = "doc-full"
        label = "Card"


class CardsBlock(blocks.StructBlock):
    section_heading = blocks.CharBlock(required=False)
    section_subheading = blocks.TextBlock(required=False)
    columns = blocks.ChoiceBlock(
        choices=[("2", "2"), ("3", "3"), ("4", "4")],
        default="3",
    )
    style = blocks.ChoiceBlock(
        choices=[
            ("default", "Default cards"),
            ("accreditation", "Standards & organizations"),
            ("pillar", "Organizational pillars"),
        ],
        default="default",
    )
    cards = blocks.ListBlock(CardItemBlock())

    class Meta:
        icon = "grip"
        label = "Cards Grid"
        template = "blocks/cards_block.html"


class VASubsectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    body = blocks.TextBlock()
    button_text = blocks.CharBlock(required=False)
    button_link = PageOrUrlLinkBlock(required=False)


class VASectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    highlight = blocks.RichTextBlock()
    intro = blocks.TextBlock(required=False)
    section_id = blocks.CharBlock(required=False, default="va-accelerator")
    subsections = blocks.ListBlock(VASubsectionBlock())

    class Meta:
        icon = "pick"
        label = "VA Accelerator Section"
        template = "blocks/va_section_block.html"


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author_name = blocks.CharBlock(required=False)
    author_title = blocks.CharBlock(required=False)
    author_image = ImageChooserBlock(
        required=False,
        help_text="Optional author photo.",
    )
    prominent = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = "openquote"
        label = "Testimonial"
        template = "blocks/testimonial_block.html"


class StatItemBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    icon = blocks.ChoiceBlock(
        choices=[
            ("shield", "Shield — Anticipate"),
            ("lightning", "Lightning — Respond"),
            ("clock", "Clock — Recover"),
            ("chart", "Chart — Sustain"),
        ],
        default="shield",
    )


class StatsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    items = blocks.ListBlock(StatItemBlock())

    class Meta:
        icon = "list-ul"
        label = "Stats / Tagline Row"
        template = "blocks/stats_block.html"


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    subheading = blocks.TextBlock(required=False)
    primary_button_text = blocks.CharBlock()
    primary_button_link = PageOrUrlLinkBlock()
    secondary_button_text = blocks.CharBlock(required=False)
    secondary_button_link = PageOrUrlLinkBlock(required=False)
    band_style = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Use full-width CTA band styling",
    )

    class Meta:
        icon = "radio-full"
        label = "Call to Action"
        template = "blocks/cta_block.html"


class PromoBlock(blocks.StructBlock):
    badge_text = blocks.CharBlock(required=False)
    heading = blocks.CharBlock()
    body = RichTextBlock()
    button_text = blocks.CharBlock(required=False)
    button_link = PageOrUrlLinkBlock(required=False)
    background_style = blocks.ChoiceBlock(
        choices=[("light", "Light"), ("dark", "Dark"), ("accent", "Accent")],
        default="accent",
    )

    class Meta:
        icon = "pick"
        label = "Promo / Highlight Section"
        template = "blocks/promo_block.html"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = RichTextBlock()


class FAQBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, default="Frequently Asked Questions")
    items = blocks.ListBlock(FAQItemBlock())

    class Meta:
        icon = "help"
        label = "FAQ Accordion"
        template = "blocks/faq_block.html"


CONTENT_BLOCK_DEFINITIONS = [
    ("hero", HeroBlock()),
    ("tabs", TabsBlock()),
    ("feature", FeatureBlock()),
    ("cards", CardsBlock()),
    ("va_section", VASectionBlock()),
    ("testimonial", TestimonialBlock()),
    ("stats", StatsBlock()),
    ("cta", CTABlock()),
    ("promo", PromoBlock()),
    ("rich_text", RichTextBlock()),
    ("faq", FAQBlock()),
]
