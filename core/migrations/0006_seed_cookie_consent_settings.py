from django.db import migrations


def seed_cookie_consent_settings(apps, schema_editor):
    from wagtail.models import Page, Site

    from core.models import CookieConsentSettings

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    settings, _created = CookieConsentSettings.objects.get_or_create(site=site_obj)
    privacy = Page.objects.filter(slug="privacy", live=True).first()

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


def clear_cookie_consent_learn_more(apps, schema_editor):
    from wagtail.models import Site

    from core.models import CookieConsentSettings

    site_obj = Site.objects.filter(is_default_site=True).first()
    if not site_obj:
        return

    settings = CookieConsentSettings.objects.filter(site=site_obj).first()
    if not settings:
        return

    settings.learn_more_link = []
    settings.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_cookie_consent_settings"),
        ("content", "0003_create_legal_pages"),
    ]

    operations = [
        migrations.RunPython(
            seed_cookie_consent_settings,
            clear_cookie_consent_learn_more,
        ),
    ]
