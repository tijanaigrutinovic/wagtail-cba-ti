from django.db import models

from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField

from core.link_blocks import LinkBlock


@register_setting
class NavigationSettings(BaseSiteSetting):
    nav_links = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
    )
    cta_button_text = models.CharField(max_length=50, default="Enroll now")
    cta_button_url = models.URLField(
        default="https://learn.cbaeducation.com/register",
    )
    login_url = models.URLField(
        default="https://learn.cbaeducation.com/login",
    )

    panels = [
        FieldPanel("nav_links"),
        FieldRowPanel([
            FieldPanel("cta_button_text"),
            FieldPanel("cta_button_url"),
        ]),
        FieldPanel("login_url"),
    ]

    class Meta:
        verbose_name = "Navigation"


@register_setting
class FooterSettings(BaseSiteSetting):
    footer_links = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
    )
    legal_links = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
        help_text="Privacy, Terms, and other legal links shown in the footer bottom row.",
    )
    copyright_text = models.CharField(
        max_length=255,
        default="2025 Center for Business Acceleration. All rights reserved.",
    )

    panels = [
        FieldPanel("footer_links"),
        FieldPanel("legal_links"),
        FieldPanel("copyright_text"),
    ]

    class Meta:
        verbose_name = "Footer"
