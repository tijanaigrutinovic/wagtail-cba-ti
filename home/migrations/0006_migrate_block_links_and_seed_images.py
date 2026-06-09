import copy
from pathlib import Path

from django.core.files.images import ImageFile
from django.db import migrations


IMAGE_FILES = {
    "hero.svg": "Home — resilience framework",
    "individual-learning.svg": "Home — individual learning tab",
    "workplace-learning.svg": "Home — workplace learning tab",
    "veteran-accelerator.svg": "Home — veteran accelerator tab",
}


def _page_id_for_path(Page, path):
    slug = path.strip("/").split("/")[-1]
    if not slug:
        return None
    page = Page.objects.filter(slug=slug, live=True).first()
    return page.id if page else None


def _url_to_link(url, page_resolver, Page):
    url = url or ""
    page_id = None
    if url.startswith("/") and not url.startswith("//") and not url.startswith("#"):
        page_id = page_resolver(url)
    if page_id:
        page = Page.objects.filter(pk=page_id).first()
        return {"page": page, "url": ""}
    return {"page": None, "url": url}


def _convert_link_fields(value, page_resolver, Page):
    value = copy.deepcopy(value)

    for old_key, new_key in (
        ("primary_button_url", "primary_button_link"),
        ("secondary_button_url", "secondary_button_link"),
        ("button_url", "button_link"),
        ("link_url", "link"),
    ):
        if old_key in value:
            value[new_key] = _url_to_link(value.pop(old_key), page_resolver, Page)

    for list_key in ("tabs", "cards", "subsections", "items"):
        if list_key not in value:
            continue
        converted = []
        for item in value[list_key]:
            if isinstance(item, dict) and "value" in item:
                inner = _convert_link_fields(item["value"], page_resolver, Page)
                converted.append(inner)
            else:
                converted.append(_convert_link_fields(item, page_resolver, Page))
        value[list_key] = converted

    if "tabs" in value:
        for tab in value["tabs"]:
            tab.setdefault("image_alt", tab.get("heading", ""))

    return value


def _homepage_seed(page_resolver, Page):
    from home.homepage_seed import SEED_BODY

    return [
        (block_type, _convert_link_fields(block_value, page_resolver, Page))
        for block_type, block_value in SEED_BODY
    ]


def _import_images(base_dir):
    from wagtail.images.models import Image

    images_dir = base_dir / "cba_site" / "static" / "cba" / "images"
    imported = {}
    for filename, title in IMAGE_FILES.items():
        path = images_dir / filename
        if not path.exists():
            continue
        existing = Image.objects.filter(title=title).first()
        if existing:
            imported[filename] = existing.id
            continue
        with path.open("rb") as handle:
            image = Image(title=title, file=ImageFile(handle, name=filename))
            image.save()
            imported[filename] = image.id
    return imported


def _assign_homepage_images(body, image_ids):
    from wagtail.images.models import Image

    body = copy.deepcopy(body)
    tab_images = [
        "individual-learning.svg",
        "workplace-learning.svg",
        "veteran-accelerator.svg",
    ]

    def image_for(filename):
        image_pk = image_ids.get(filename)
        if not image_pk:
            return None
        return Image.objects.filter(pk=image_pk).first()

    for index, (block_type, value) in enumerate(body):
        if block_type == "feature" and not value.get("image"):
            value["image"] = image_for("hero.svg")
            body[index] = (block_type, value)
        elif block_type == "tabs":
            for tab_index, tab in enumerate(value.get("tabs", [])):
                if not tab.get("image") and tab_index < len(tab_images):
                    tab["image"] = image_for(tab_images[tab_index])
            body[index] = (block_type, value)

    return body


def _needs_rebuild(homepage):
    if not homepage.body:
        return True
    for block in homepage.body.raw_data:
        if block["type"] != "hero":
            continue
        value = block["value"]
        if "primary_button_url" in value:
            return True
        link = value.get("primary_button_link") or {}
        if not link.get("url") and not link.get("page"):
            return True
    return False


def migrate_stream_links_and_images(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    HomePage = apps.get_model("home", "HomePage")
    FlexPage = apps.get_model("content", "FlexPage")

    base_dir = Path(__file__).resolve().parents[2]

    def page_resolver(path):
        return _page_id_for_path(Page, path)

    homepage = HomePage.objects.filter(slug="home").first()
    if homepage and _needs_rebuild(homepage):
        body = _homepage_seed(page_resolver, Page)
        try:
            image_ids = _import_images(base_dir)
            if image_ids:
                body = _assign_homepage_images(body, image_ids)
        except Exception:
            pass
        homepage.body = body
        homepage.save(update_fields=["body"])
    elif homepage and homepage.body:
        migrated_body = []
        for block in homepage.body.raw_data:
            block_type = block["type"]
            value = _convert_link_fields(block["value"], page_resolver, Page)
            migrated_body.append((block_type, value))
        homepage.body = migrated_body
        homepage.save(update_fields=["body"])

    for page in FlexPage.objects.exclude(body__isnull=True).exclude(body=""):
        if not page.body:
            continue
        migrated = []
        for block in page.body.raw_data:
            block_type = block["type"]
            value = _convert_link_fields(block["value"], page_resolver, Page)
            migrated.append((block_type, value))
        page.body = migrated
        page.save(update_fields=["body"])


def reverse_migration(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_block_links_and_images"),
        ("content", "0002_block_links_and_images"),
        ("wagtailcore", "0002_initial_data"),
    ]

    operations = [
        migrations.RunPython(migrate_stream_links_and_images, reverse_migration),
    ]
