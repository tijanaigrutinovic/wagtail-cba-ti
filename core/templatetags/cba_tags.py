from django import template

register = template.Library()


def _resolve_link(link):
    if not link:
        return ""
    page = link.get("page") if isinstance(link, dict) else getattr(link, "page", None)
    if page:
        specific = page.specific if hasattr(page, "specific") else page
        return specific.url if hasattr(specific, "url") else page.url
    url = link.get("url") if isinstance(link, dict) else getattr(link, "url", None)
    return (url or "").strip()


@register.simple_tag
def resolve_link_url(link):
    """Return href for a link block value (page chooser or raw URL)."""
    return _resolve_link(link) or "#"


@register.filter
def link_url(link):
    """Return resolved href or empty string (for {% if %} checks)."""
    return _resolve_link(link)


@register.simple_tag
def cms_image_url(image):
    """Return the media URL for a Wagtail image."""
    if not image:
        return ""
    return image.file.url
