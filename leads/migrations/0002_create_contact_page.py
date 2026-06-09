from django.db import migrations


def create_contact_page(apps, schema_editor):
    from home.models import HomePage
    from leads.models import ContactFormField, ContactPage

    home = HomePage.objects.filter(slug="home").first()
    if not home or ContactPage.objects.filter(slug="contact").exists():
        return

    contact = ContactPage(
        title="Contact Us",
        draft_title="Contact Us",
        slug="contact",
        intro_heading="Get in Touch",
        intro_text=(
            "Ready to advance your career? Contact us today to learn more about our "
            "professional development programs and certification courses."
        ),
        thank_you_text=(
            "<p>Thank you for contacting CBA Education. We have received your message "
            "and will respond within one business day.</p>"
        ),
        to_address="support@cbaccel.com",
        from_address="noreply@cbaeducation.com",
        subject="New contact form submission",
    )
    home.add_child(instance=contact)

    form_fields = [
        ("first_name", "singleline", "First Name", True, ""),
        ("last_name", "singleline", "Last Name", True, ""),
        ("email", "email", "Email Address", True, ""),
        ("confirm_email", "email", "Confirm Email", True, ""),
        ("phone", "singleline", "Phone Number", False, ""),
        (
            "reason",
            "dropdown",
            "Reason for Contacting",
            True,
            "General Inquiry,Course Information,Program Information,"
            "Technical Support,Other",
        ),
        ("company", "singleline", "Company / Organization", False, ""),
        ("message", "multiline", "Message", True, ""),
    ]

    for sort_order, (name, field_type, label, required, choices) in enumerate(form_fields):
        ContactFormField.objects.create(
            page=contact,
            sort_order=sort_order,
            clean_name=name,
            label=label,
            field_type=field_type,
            required=required,
            choices=choices,
            default_value="",
        )

    contact.faq_section = [
        (
            "faq",
            {
                "heading": "Maybe we have ready answers for you in the FAQ ? Find it!",
                "items": [
                    {
                        "question": "Curriculum information",
                        "answer": (
                            "<p>Our curriculums contain courselets™, knowledge checks, "
                            "lab assignments, reading assignments, webinars, and calls with "
                            "facilitators.</p>"
                        ),
                    },
                    {
                        "question": "Address and Phone Number",
                        "answer": (
                            "<p><strong>Center for Business Acceleration</strong></p>"
                            "<p>6440 Sky Pointe Dr #140-550<br>"
                            "Las Vegas Nevada, 89131</p>"
                            "<p><strong>Phone:</strong> (240) 715-6200</p>"
                        ),
                    },
                ],
            },
        ),
    ]
    contact.save()
    contact.save_revision().publish()


def remove_contact_page(apps, schema_editor):
    from leads.models import ContactPage

    ContactPage.objects.filter(slug="contact").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0001_initial"),
        ("home", "0004_populate_homepage_body"),
    ]

    operations = [
        migrations.RunPython(create_contact_page, remove_contact_page),
    ]
