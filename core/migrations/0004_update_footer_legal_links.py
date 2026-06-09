from django.db import migrations


def update_footer_legal_links(apps, schema_editor):
    from wagtail.models import Page

    from core.models import FooterSettings

    site = Page.objects.filter(depth=1).first()
    if not site:
        from wagtail.models import Site

        site_obj = Site.objects.filter(is_default_site=True).first()
        if not site_obj:
            return
    else:
        from wagtail.models import Site

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
                "url": "" if privacy else "/privacy",
            },
        ),
        (
            "link",
            {
                "label": "Terms",
                "page": terms,
                "url": "" if terms else "/terms",
            },
        ),
    ]
    footer.save()


def restore_footer_legal_links(apps, schema_editor):
    from wagtail.models import Site

    from core.models import FooterSettings

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    footer = FooterSettings.objects.filter(site=site_obj).first()
    if not footer:
        return

    footer.legal_links = [
        ("link", {"label": "Privacy", "page": None, "url": "/privacy"}),
        ("link", {"label": "Terms", "page": None, "url": "/terms"}),
        ("link", {"label": "Cookies", "page": None, "url": "/cookies"}),
    ]
    footer.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_block_links_and_images"),
        ("content", "0003_create_legal_pages"),
    ]

    operations = [
        migrations.RunPython(update_footer_legal_links, restore_footer_legal_links),
    ]
