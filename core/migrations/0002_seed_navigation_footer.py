from django.db import migrations


def seed_site_settings(apps, schema_editor):
    Site = apps.get_model("wagtailcore", "Site")
    NavigationSettings = apps.get_model("core", "NavigationSettings")
    FooterSettings = apps.get_model("core", "FooterSettings")

    site = Site.objects.filter(is_default_site=True).first()
    if not site:
        return

    nav, _ = NavigationSettings.objects.get_or_create(site=site)
    if not nav.nav_links:
        nav.nav_links = [
            ("link", {"label": "About", "page": None, "url": "/about"}),
            ("link", {"label": "Catalog", "page": None, "url": "/courses"}),
            ("link", {"label": "Our Programs", "page": None, "url": "/programs"}),
            ("link", {"label": "Credentialing", "page": None, "url": "/credentialing"}),
            ("link", {"label": "Contact Us", "page": None, "url": "/contact"}),
        ]
        nav.cta_button_text = "Enroll now"
        nav.cta_button_url = "https://learn.cbaeducation.com/register"
        nav.login_url = "https://learn.cbaeducation.com/login"
        nav.save()

    footer, _ = FooterSettings.objects.get_or_create(site=site)
    if not footer.footer_links:
        footer.footer_links = [
            ("link", {"label": "About", "page": None, "url": "/about"}),
            ("link", {"label": "Catalog", "page": None, "url": "/courses"}),
            ("link", {"label": "Our Programs", "page": None, "url": "/programs"}),
            ("link", {"label": "Credentialing", "page": None, "url": "/credentialing"}),
            ("link", {"label": "Contact Us", "page": None, "url": "/contact"}),
        ]
        footer.legal_links = [
            ("link", {"label": "Privacy", "page": None, "url": "/privacy"}),
            ("link", {"label": "Terms", "page": None, "url": "/terms"}),
        ]
        footer.copyright_text = (
            "2025 Center for Business Acceleration. All rights reserved."
        )
        footer.save()


def clear_site_settings(apps, schema_editor):
    NavigationSettings = apps.get_model("core", "NavigationSettings")
    FooterSettings = apps.get_model("core", "FooterSettings")
    NavigationSettings.objects.all().delete()
    FooterSettings.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("wagtailcore", "0002_initial_data"),
    ]

    operations = [
        migrations.RunPython(seed_site_settings, clear_site_settings),
    ]
