from pathlib import Path

from bs4 import BeautifulSoup
from django.db import migrations


def import_faq_from_static(apps, schema_editor):
    from leads.models import ContactPage

    contact = ContactPage.objects.filter(slug="contact").first()
    if not contact:
        return

    static_path = (
        Path(__file__).resolve().parents[2]
        / "cba_site"
        / "templates"
        / "cba"
        / "pages"
        / "contact.html"
    )
    if not static_path.exists():
        return

    soup = BeautifulSoup(static_path.read_text(), "html.parser")
    faq_section = soup.select_one("#faq")
    if not faq_section:
        return

    heading_el = faq_section.select_one("h2")
    heading = heading_el.get_text(strip=True) if heading_el else "Frequently Asked Questions"

    items = []
    for faq_item in faq_section.select(".faq-item"):
        question_btn = faq_item.select_one(".faq-question")
        answer_div = faq_item.select_one(".faq-answer")
        if not question_btn or not answer_div:
            continue
        for icon in question_btn.select("i"):
            icon.decompose()
        question = question_btn.get_text(strip=True)
        answer = "".join(str(child) for child in answer_div.children).strip()
        if question and answer:
            items.append({"question": question, "answer": answer})

    if not items:
        return

    contact.faq_section = [("faq", {"heading": heading, "items": items})]
    contact.save()
    contact.save_revision().publish()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0002_create_contact_page"),
    ]

    operations = [
        migrations.RunPython(import_faq_from_static, noop),
    ]
