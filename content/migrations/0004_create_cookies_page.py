from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from django.db import migrations


def _cookies_template_path():
    return Path(__file__).resolve().parents[1] / "legal_seed" / "cookies.html"


def _extract_badges(soup, badge_class):
    badges = []
    for badge in soup.select(f".{badge_class} .badge"):
        label = badge.get_text(strip=True)
        if label:
            badges.append(("badge", {"label": label, "description": ""}))
    return badges


def _extract_body_html(soup, content_class):
    column = soup.select_one(f".{content_class} .col-12")
    if not column:
        return ""
    for el in column.select(".text-center.mb-5"):
        el.decompose()
    return column.decode_contents().strip()


def _update_cookie_banner_link(cookies_page):
    from wagtail.models import Site

    from core.models import CookieConsentSettings

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    settings = CookieConsentSettings.objects.filter(site=site_obj).first()
    if not settings:
        return

    settings.learn_more_link = [
        (
            "link",
            {
                "label": "Learn more",
                "page": cookies_page,
                "url": "" if cookies_page else "/cookies/",
            },
        ),
    ]
    settings.save()


def _update_footer_cookies_link(cookies_page):
    from wagtail.models import Page, Site

    from core.models import FooterSettings

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    footer = FooterSettings.objects.filter(site=site_obj).first()
    if not footer:
        return

    privacy = Page.objects.filter(slug="privacy", live=True).first()
    terms = Page.objects.filter(slug="terms", live=True).first()

    footer.legal_links = [
        (
            "link",
            {
                "label": "Privacy",
                "page": privacy,
                "url": "" if privacy else "/privacy/",
            },
        ),
        (
            "link",
            {
                "label": "Terms",
                "page": terms,
                "url": "" if terms else "/terms/",
            },
        ),
        (
            "link",
            {
                "label": "Cookies",
                "page": cookies_page,
                "url": "" if cookies_page else "/cookies/",
            },
        ),
    ]
    footer.save()


def create_cookies_page(apps, schema_editor):
    from content.models import LegalPage
    from home.models import HomePage

    home = HomePage.objects.filter(slug="home").first()
    if not home:
        return

    cookies_path = _cookies_template_path()
    if not cookies_path.exists():
        return

    if LegalPage.objects.filter(slug="cookies").exists():
        cookies_page = LegalPage.objects.get(slug="cookies")
    else:
        cookies_soup = BeautifulSoup(cookies_path.read_text(), "html.parser")
        intro_el = cookies_soup.select_one(".cookies-hero p")
        cookies_page = LegalPage(
            title="Cookie Policy",
            draft_title="Cookie Policy",
            slug="cookies",
            intro=intro_el.get_text(strip=True) if intro_el else "",
            compliance_badges=_extract_badges(cookies_soup, "cookies-badges"),
            last_updated=date(2026, 6, 9),
            body=_extract_body_html(cookies_soup, "cookies-content"),
        )
        home.add_child(instance=cookies_page)
        cookies_page.save_revision().publish()

    _update_cookie_banner_link(cookies_page)
    _update_footer_cookies_link(cookies_page)


def remove_cookies_page(apps, schema_editor):
    from wagtail.models import Page, Site

    from content.models import LegalPage
    from core.models import CookieConsentSettings, FooterSettings

    LegalPage.objects.filter(slug="cookies").delete()

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    privacy = Page.objects.filter(slug="privacy", live=True).first()

    settings = CookieConsentSettings.objects.filter(site=site_obj).first()
    if settings:
        settings.learn_more_link = [
            (
                "link",
                {
                    "label": "Learn more",
                    "page": privacy,
                    "url": "" if privacy else "/privacy/",
                },
            ),
        ]
        settings.save()

    footer = FooterSettings.objects.filter(site=site_obj).first()
    if footer:
        terms = Page.objects.filter(slug="terms", live=True).first()
        footer.legal_links = [
            (
                "link",
                {
                    "label": "Privacy",
                    "page": privacy,
                    "url": "" if privacy else "/privacy/",
                },
            ),
            (
                "link",
                {
                    "label": "Terms",
                    "page": terms,
                    "url": "" if terms else "/terms/",
                },
            ),
        ]
        footer.save()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0003_create_legal_pages"),
        ("core", "0006_seed_cookie_consent_settings"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.RunPython(create_cookies_page, remove_cookies_page),
    ]
