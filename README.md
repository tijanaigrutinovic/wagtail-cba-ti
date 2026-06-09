# CBA Education — Wagtail CMS

Public marketing website for [cbaeducation.com](https://cbaeducation.com), part of the CBA Education future-state architecture:

| Domain | System | Purpose |
|---|---|---|
| `cbaeducation.com` | **This repo (Wagtail)** | Homepage, catalog, blog, forms, SEO |
| `learn.cbaeducation.com` | Open edX LMS | Auth, enrollment, courseware, certificates |
| `studio.cbaeducation.com` | Open edX CMS | Course authoring |

## Current milestone (`main` branch)

Wagtail installation and project scaffold only — ready for DigitalOcean deployment per the implementation runbook (sections 3–5).

**Included:**
- Wagtail 7.4 + Django 6 project (`cba_site`)
- App stubs: `home`, `core`, `content`, `catalog`, `programs`, `blog`, `leads`
- Settings split: `dev` (SQLite) / `production` (PostgreSQL + environ)
- `.env.example` with Open edX and email placeholders
- Reference deploy configs in `deploy/` (Nginx, systemd, PostgreSQL)

**Not included yet** (separate branches / milestones):
- StreamField blocks and page models
- Navigation/Footer site settings
- Public-facing pages (Home, Legal, Contact, Catalog, Courses, Programs)
- Open edX catalog sync service
- Blog, SEO, search

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/

Uses SQLite and console email backend by default (`cba_site.settings.dev`).

## Production deployment (DigitalOcean)

Follow runbook section 5 on a separate Droplet from Open edX:

1. Ubuntu 24.04, 2 vCPU, 4 GB RAM (minimum)
2. Clone repo to `/srv/cba-wagtail`
3. Create venv, `pip install -r requirements.txt`
4. PostgreSQL — see `deploy/postgresql/init.sql`
5. Copy `.env.example` → `.env`, fill secrets, `chmod 600 .env`
6. `python manage.py migrate --settings=cba_site.settings.production`
7. `python manage.py collectstatic --noinput --settings=cba_site.settings.production`
8. Gunicorn — `deploy/systemd/cba-wagtail.service`
9. Nginx — `deploy/nginx/cbaeducation.com.conf`
10. SSL — `sudo certbot --nginx -d cbaeducation.com -d www.cbaeducation.com`

### DNS (runbook section 4)

| Hostname | Target |
|---|---|
| `cbaeducation.com` | Wagtail Droplet IP |
| `www.cbaeducation.com` | CNAME → `cbaeducation.com` |
| `learn.cbaeducation.com` | Open edX LMS IP |
| `studio.cbaeducation.com` | Open edX CMS IP |

Keep `edavantage.com` active during migration; add 301 redirects after validation.

## Environment variables

See `.env.example`. Key production values:

- `DATABASE_URL` — PostgreSQL connection string
- `OPENEDX_BASE_URL` — `https://learn.cbaeducation.com`
- `OPENEDX_STUDIO_URL` — `https://studio.cbaeducation.com`

## Mobile app safety

Wagtail must **not** replace LMS routes. Navigation CTAs should link only to safe Open edX URLs:

- Login: `https://learn.cbaeducation.com/login`
- Register: `https://learn.cbaeducation.com/register`
- Dashboard: `https://learn.cbaeducation.com/dashboard`

Do not redirect `/course/*` or `/certificates/*` to Wagtail.

## Project structure

```
cba_site/          # Django project settings, urls, wsgi
home/              # Homepage (default Wagtail starter)
core/              # Shared StreamField blocks (future)
content/           # FlexPage, LegalPage (future)
catalog/           # Courses, programs, API sync (future)
programs/          # Certificate programs, waitlists (future)
blog/              # Blog (future)
leads/             # Contact forms (future)
search/            # Wagtail search
deploy/            # Nginx, systemd, PostgreSQL reference configs
```
