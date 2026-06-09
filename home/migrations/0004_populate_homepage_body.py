from django.db import migrations


def populate_homepage(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    homepage = HomePage.objects.filter(slug="home").first()
    if not homepage or homepage.body:
        return

    homepage.body = [
        ("hero", {
            "heading": "Can you Afford to Be Unprepared?",
            "subheading": (
                "In today's complex world, unmanaged risk can derail even the strongest "
                "organizations. We help you build organizational resilience through strong "
                "governance & leadership, enterprise risk management, and business continuity "
                "— so you can protect value and thrive under disruption."
            ),
            "primary_button_text": "Take a course",
            "primary_button_url": "/courses",
            "secondary_button_text": "Enroll in a Certificate Program",
            "secondary_button_url": "/programs",
            "background_image": None,
            "background_image_alt": "Global network and technology visualization",
        }),
        ("tabs", {
            "section_heading": "Accelerate your Learning",
            "section_subheading": (
                "Learn on your own, upskill your team, or build what's next — pick the track "
                "that fits how you work."
            ),
            "section_id": "programs",
            "tabs": [
                {
                    "tab_label": "Individual learning",
                    "heading": "Take a course or earn a certificate",
                    "body": (
                        "Apply international standards in real operations — complete a single "
                        "course or earn a full certificate you can take anywhere."
                    ),
                    "button_text": "Explore individual learning",
                    "button_url": "/courses",
                    "image": None,
                },
                {
                    "tab_label": "Workplace learning",
                    "heading": "Grow as a Team",
                    "body": (
                        "Support your employees' growth with targeted, skill-based training. "
                        "Whether you're upskilling a department or onboarding new team members, "
                        "our workplace programs deliver measurable results."
                    ),
                    "button_text": "Discover workplace learning",
                    "button_url": "/programs",
                    "image": None,
                },
                {
                    "tab_label": "Veteran accelerator",
                    "heading": "Build Your Next Chapter",
                    "body": (
                        "Our VA Accelerator program is designed to recognize your experience "
                        "and help you move forward with confidence. Transition into a stable "
                        "career or become self-employed with a clear pathway through comprehensive "
                        "academics leading to a valued certificate."
                    ),
                    "button_text": "Explore the VA Accelerator",
                    "button_url": "#va-accelerator",
                    "image": None,
                },
            ],
        }),
        ("feature", {
            "image": None,
            "image_position": "left",
            "heading": "Why resilience matters",
            "subheading": (
                "How strategy, trust, and continuity connect — from objectives and decisions "
                "to protection under disruption."
            ),
            "body": (
                "<p>Unmanaged risk slows momentum. Organizations that identify threats early, "
                "build continuity, and train leaders recover faster and scale with confidence.</p>"
                "<p>This program gives your team a shared language for risk, compliance, and "
                "operational readiness — so acceleration is sustainable, not fragile.</p>"
            ),
            "outcomes_heading": "What you'll achieve",
            "outcomes": [
                "Identify and assess risks early — before they become crises",
                "Build continuity plans that teams can actually run",
                "Align leadership decisions with sector-specific standards",
                "Demonstrate quality assurance to stakeholders & partners",
            ],
            "button_text": "",
            "button_url": "",
        }),
        ("cards", {
            "section_heading": "Standards & organizations",
            "section_subheading": (
                "Our Education maps to frameworks from recognized standards bodies — open each "
                "card to read more on the official site."
            ),
            "columns": "4",
            "style": "accreditation",
            "cards": [
                {
                    "icon": None,
                    "heading": "ACCET",
                    "body": "U.S. accreditation for continuing education and training providers.",
                    "link_text": "",
                    "link_url": "https://accet.org/",
                    "link_meta": "accet.org",
                    "external_link": True,
                },
                {
                    "icon": None,
                    "heading": "ISO",
                    "body": "International standards for management systems, risk, and quality.",
                    "link_text": "",
                    "link_url": "https://www.iso.org/home.html",
                    "link_meta": "iso.org",
                    "external_link": True,
                },
                {
                    "icon": None,
                    "heading": "ANSI",
                    "body": "U.S. hub for voluntary consensus and adopted standards.",
                    "link_text": "",
                    "link_url": "https://webstore.ansi.org/standards/astm/astme265924",
                    "link_meta": "webstore.ansi.org",
                    "external_link": True,
                },
                {
                    "icon": None,
                    "heading": "ASTM",
                    "body": "Technical standards referenced across operations and resilience.",
                    "link_text": "",
                    "link_url": "https://store.astm.org/e3502-25.html",
                    "link_meta": "store.astm.org",
                    "external_link": True,
                },
            ],
        }),
        ("cards", {
            "section_heading": "Build Organizational Resilience",
            "section_subheading": "",
            "columns": "3",
            "style": "pillar",
            "cards": [
                {
                    "icon": None,
                    "heading": "Governance & Leadership",
                    "body": (
                        "Strategic oversight, leadership commitment, policy frameworks, and "
                        "integration of resilience into culture, strategy, and decision-making."
                    ),
                    "link_text": "Learn more →",
                    "link_url": "/contact",
                    "link_meta": "",
                    "external_link": False,
                },
                {
                    "icon": None,
                    "heading": "Risk Management",
                    "body": (
                        "Systematic identification, assessment, treatment, and monitoring of risks "
                        "— including emerging risks — to protect and create value."
                    ),
                    "link_text": "Learn more →",
                    "link_url": "/contact",
                    "link_meta": "",
                    "external_link": False,
                },
                {
                    "icon": None,
                    "heading": "Operational Resilience",
                    "body": (
                        "Business continuity, incident and emergency management, security, and "
                        "facility operations to maintain performance under disruption."
                    ),
                    "link_text": "Learn more →",
                    "link_url": "/contact",
                    "link_meta": "",
                    "external_link": False,
                },
            ],
        }),
        ("va_section", {
            "heading": "VA Accelerator™",
            "highlight": "<p>The <strong>VA Accelerator Tuition</strong> is solely funded through Grants.</p>",
            "intro": (
                "Our Education maps to frameworks from recognized standards bodies — open each "
                "card to read more on the official site."
            ),
            "section_id": "va-accelerator",
            "subsections": [
                {
                    "heading": "Certificate Programs",
                    "body": (
                        "Our certificate programs are designed to equip you with in-demand skills "
                        "and practical knowledge to advance your career or explore a new field. "
                        "Whether you're upskilling or reskilling, our flexible, expert-led courses "
                        "will help you reach your goals."
                    ),
                    "button_text": "Explore certificate programs",
                    "button_url": "/programs",
                },
                {
                    "heading": "Personal Certifications",
                    "body": (
                        "Invest in yourself! Our personal certification programs make it easy to "
                        "build confidence, sharpen your skills, and achieve your goals on your schedule. "
                        "Whether you're aiming for a promotion, a new job, or personal growth, "
                        "we're here to help you succeed."
                    ),
                    "button_text": "Explore personal certifications",
                    "button_url": "/courses",
                },
            ],
        }),
        ("testimonial", {
            "quote": (
                "Participants gain the clarity to lead decisively and accelerate organizational "
                "performance."
            ),
            "author_name": "",
            "author_title": "",
            "author_image": None,
            "prominent": True,
        }),
        ("stats", {
            "heading": "The Acceleration You Gain",
            "items": [
                {"label": "Anticipate risks early", "icon": "shield"},
                {"label": "Respond with clarity", "icon": "lightning"},
                {"label": "Recover faster", "icon": "clock"},
                {"label": "Sustain performance", "icon": "chart"},
            ],
        }),
        ("cta", {
            "heading": "Don't let unmanaged risk slow your momentum.",
            "subheading": "",
            "primary_button_text": "Explore programs & enroll →",
            "primary_button_url": "/courses",
            "secondary_button_text": "Request guidance",
            "secondary_button_url": "/contact",
            "band_style": True,
        }),
    ]
    homepage.save()


def clear_homepage(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    homepage = HomePage.objects.filter(slug="home").first()
    if homepage:
        homepage.body = []
        homepage.save()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_homepage_body"),
    ]

    operations = [
        migrations.RunPython(populate_homepage, clear_homepage),
    ]
