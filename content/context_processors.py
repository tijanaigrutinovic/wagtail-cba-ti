from django.conf import settings


def cba_site(request):
    return {
        "OPENEDX_BASE_URL": getattr(
            settings, "OPENEDX_BASE_URL", "https://learn.cbaeducation.com"
        ),
        "OPENEDX_STUDIO_URL": getattr(
            settings, "OPENEDX_STUDIO_URL", "https://studio.cbaeducation.com"
        ),
    }
