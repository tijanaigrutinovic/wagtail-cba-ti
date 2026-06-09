from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from django.db import migrations


def _legal_template_paths():
    seed_dir = Path(__file__).resolve().parents[1] / "legal_seed"
    return seed_dir / "privacy.html", seed_dir / "terms.html"


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


def _create_legal_page(home, spec):
    from content.models import LegalPage

    if LegalPage.objects.filter(slug=spec["slug"]).exists():
        return LegalPage.objects.get(slug=spec["slug"])

    page = LegalPage(
        title=spec["title"],
        draft_title=spec["title"],
        slug=spec["slug"],
        intro=spec["intro"],
        compliance_badges=spec["badges"],
        last_updated=spec["last_updated"],
        body=spec["body"],
    )
    home.add_child(instance=page)
    page.save_revision().publish()
    return page


def create_legal_pages(apps, schema_editor):
    from home.models import HomePage

    home = HomePage.objects.filter(slug="home").first()
    if not home:
        return

    privacy_path, terms_path = _legal_template_paths()

    if privacy_path.exists():
        privacy_soup = BeautifulSoup(privacy_path.read_text(), "html.parser")
        intro_el = privacy_soup.select_one(".privacy-hero p")
        _create_legal_page(
            home,
            {
                "title": "Privacy Policy",
                "slug": "privacy",
                "intro": intro_el.get_text(strip=True) if intro_el else "",
                "badges": _extract_badges(privacy_soup, "privacy-badges"),
                "last_updated": date(2025, 1, 15),
                "body": _extract_body_html(privacy_soup, "privacy-content"),
            },
        )

    if terms_path.exists():
        terms_soup = BeautifulSoup(terms_path.read_text(), "html.parser")
        intro_el = terms_soup.select_one(".terms-hero p")
        _create_legal_page(
            home,
            {
                "title": "Terms of Service",
                "slug": "terms",
                "intro": intro_el.get_text(strip=True) if intro_el else "",
                "badges": _extract_badges(terms_soup, "terms-badges"),
                "last_updated": date(2025, 1, 15),
                "body": _extract_body_html(terms_soup, "terms-content"),
            },
        )


def remove_legal_pages(apps, schema_editor):
    from content.models import LegalPage

    LegalPage.objects.filter(slug__in=["privacy", "terms"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0002_block_links_and_images"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.RunPython(create_legal_pages, remove_legal_pages),
    ]
