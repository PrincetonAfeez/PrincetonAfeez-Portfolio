# princetonafeez.com

A personal portfolio site that catalogues a hospitality operator's transition into Python and system architecture. Built as a Django + HTMX monolith, deployed to Railway, served at [princetonafeez.com](https://princetonafeez.com).

[![CI](https://github.com/PrincetonAfeez/princetonafeez.com/actions/workflows/ci.yml/badge.svg)](https://github.com/PrincetonAfeez/princetonafeez.com/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)
[![Coverage](https://img.shields.io/badge/coverage-70%25%2B-brightgreen.svg)](#testing)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Looking for the live site?

If you arrived here by accident and you're looking for Princeton Afeez's professional portfolio, the live site is at **[princetonafeez.com](https://princetonafeez.com)**.

This repository is the source code. Everything below is for engineers reading the code or future-Princeton returning to maintain it.

---

## Table of contents

- [What this is](#what-this-is)
- [Architecture at a glance](#architecture-at-a-glance)
- [Quick start](#quick-start)
- [Project structure](#project-structure)
- [Development workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)
- [Adding an app to the catalogue](#adding-an-app-to-the-catalogue)
- [Documentation index](#documentation-index)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

---

## What this is

A personal portfolio website that serves two distinct audiences.

**The primary audience** is hospitality decision-makers — restaurant owners, group operators, regional directors, hospitality recruiters — evaluating Princeton for senior General Manager, Multi-Unit GM, Area Manager, and Regional Director roles. For them, the site leads with thirty-five years of hospitality experience, ten-plus years of multi-unit P&L ownership, and quantified outcomes across roles at Crawford's Social, Lucky Baldwins, Latte Republique, and other Los Angeles operations.

**The secondary audience** is technical readers — engineers, hiring managers, accelerator reviewers, and self-taught developers — who may discover Princeton through the technical portfolio. For them, the site catalogues every Python application Princeton has built or plans to build, with consistent five-section documentation per app (Architecture Decision Record, Technical Design Document, Interface Design Specification, Runbook, Lessons Learned).

The site itself is the first Django + HTMX application Princeton has shipped to production. It is also the capstone project for twelve months of self-directed study in Python and system architecture. The choices documented here — the architecture, the data model, the deployment, the observability — are the artifact, not just the means.

A more complete description of the site's purpose, audience, and information architecture lives in [`docs/SPEC.md`](docs/SPEC.md).

---

## Architecture at a glance

```
        ┌─────────────────────────────────────────────────┐
        │  Browser                                        │
        │  ├── Initial request → Full HTML page           │
        │  └── Scroll-triggered → HTMX partial swap       │
        └─────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────┐
        │  Django 5 (Python 3.12)                         │
        │  ├── pages/      Static marketing surface       │
        │  └── portfolio/  Dynamic apps catalogue         │
        └─────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────┐
        │  PostgreSQL 16                                  │
        │  ├── App, Stack, Concept                        │
        │  └── M2M relationships                          │
        └─────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────┐
        │  Railway (host) ← GoDaddy (registrar)           │
        │  ├── HTTPS, auto-deploy from main               │
        │  └── stdout → Railway log aggregation           │
        └─────────────────────────────────────────────────┘
```

| Layer | Choice |
|---|---|
| Language | Python 3.12 |
| Web framework | Django 5 |
| Interactivity | HTMX (CDN) |
| Database (prod) | PostgreSQL 16 |
| Database (dev) | SQLite |
| Styling | Tailwind CSS (Play CDN in v1, compiled in v1.1) |
| Icons | Lucide |
| Application server | Gunicorn |
| Static files | WhiteNoise |
| Hosting | Railway |
| Registrar | GoDaddy |
| Logging | `python-json-logger` (prod) + standard library (dev) |
| Error monitoring | Sentry |
| Testing | pytest, pytest-django, coverage |
| Linting | ruff |
| Formatting | black |
| Template linting | djlint |
| CI | GitHub Actions |

Every meaningful architectural choice is documented as an Architecture Decision Record. See [`docs/adr/`](docs/adr/) for the full set.

---

## Quick start

Prerequisites:

- Python 3.12
- pip
- Git

Clone and set up:

```bash
git clone https://github.com/PrincetonAfeez/princetonafeez.com.git
cd princetonafeez.com

python -m venv .venv
source .venv/bin/activate            # macOS / Linux
# .venv\Scripts\activate             # Windows

pip install -r requirements/dev.txt

cp .env.example .env
# Open .env and set SECRET_KEY (any 50+ random characters for local dev)

python manage.py migrate
python manage.py seed_apps           # populates the catalogue from content/apps.yaml
python manage.py createsuperuser     # optional, only if you need admin access locally

python manage.py runserver
```

The site is now running at `http://127.0.0.1:8000/`.

The default settings module for local development is `core.settings.dev`. It uses SQLite, debug mode, console logging with human-readable formatting, and a relaxed CSP that allows the Django Debug Toolbar.

---

## Project structure

```
princetonafeez.com/
├── .env.example                     # Documented env vars (gitignored .env in practice)
├── .github/workflows/ci.yml         # GitHub Actions CI pipeline
├── content/apps.yaml                # Canonical catalogue manifest (source of truth)
├── docs/
│   ├── SPEC.md                      # Full project specification
│   └── adr/                         # Architecture Decision Records (0001–0007)
├── core/                            # Django project: settings, URLs, logging, ASGI/WSGI
│   ├── settings/
│   │   ├── base.py                  # Shared defaults
│   │   ├── dev.py                   # Local development overrides
│   │   └── prod.py                  # Production overrides (Railway)
│   ├── context_processors.py        # SITE_NAME, SITE_VERSION, IS_PROD, NAV_ITEMS
│   ├── logging_config.py            # build_logging_config(is_prod) → LOGGING dict
│   └── urls.py
├── pages/                           # Static marketing surface
│   ├── views.py                     # home, about, contact, 404, 500
│   ├── content.py                   # NAV_ITEMS, FOOTER_LINKS, SITE_NAME, etc.
│   ├── templatetags/nav_tags.py     # {% active_link %}
│   └── templates/                   # base.html, layouts/, pages/, components/, sections/
├── portfolio/                       # Dynamic apps catalogue
│   ├── models.py                    # App, Stack, Concept
│   ├── views.py                     # app_list (with HTMX partial), app_detail
│   ├── templatetags/doc_tags.py     # {% doc_url app 'ADR' %}
│   ├── management/commands/
│   │   └── seed_apps.py             # Reads content/apps.yaml, upserts the DB
│   └── templates/portfolio/         # app_list.html, app_detail.html, partials/
├── manage.py
├── pyproject.toml                   # Tool configuration (ruff, black, djlint, pytest)
├── railway.toml                     # Railway deploy config
├── requirements/
│   ├── base.txt                     # Shared dependencies
│   ├── dev.txt                      # base + dev-only (debug toolbar, pytest, ruff, etc.)
│   └── prod.txt                     # base + prod-only (gunicorn, psycopg, sentry, etc.)
└── VERSION                          # Site version string, read by context processor
```

Two Django apps inside one project: `pages` (the static marketing pages) and `portfolio` (the dynamic catalogue). Clean separation of concerns.

The directory tree, with rationale for each layer, is documented in [`docs/SPEC.md`](docs/SPEC.md#7-project-structure).

---

## Development workflow

### Run the dev server

```bash
python manage.py runserver
```

### Run with a fresh database

```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_apps
```

### Make a change to the catalogue

The catalogue is version-controlled in [`content/apps.yaml`](content/apps.yaml). To add or modify an app:

1. Edit `content/apps.yaml` (see [Adding an app to the catalogue](#adding-an-app-to-the-catalogue))
2. Run `python manage.py seed_apps`
3. Commit the YAML change. The deploy pipeline re-runs `seed_apps` automatically.

Why a manifest instead of the Django admin: see [ADR-0007](docs/adr/0007-content-sync-via-manifest.md).

### Lint, format, check

```bash
ruff check .                          # Lint Python
black --check .                       # Check formatting
djlint pages/templates portfolio/templates --check  # Lint templates

# Apply fixes
ruff check . --fix
black .
djlint pages/templates portfolio/templates --reformat
```

### Pre-commit (optional, recommended)

A `.pre-commit-config.yaml` ships with the repo. To install:

```bash
pip install pre-commit
pre-commit install
```

Hooks run `ruff`, `black`, and `djlint` on every commit.

---

## Testing

Tests live under each Django app's `tests/` directory and run via `pytest`.

```bash
pytest                                # Run all tests
pytest --cov=. --cov-report=term      # With coverage report
pytest --cov=. --cov-fail-under=70    # Fail if coverage drops below 70%

pytest portfolio/tests/test_models.py  # Run a single file
pytest -k "doc_url"                   # Run tests matching a name
```

The CI pipeline enforces a 70% line coverage minimum. The build fails if coverage drops below that threshold.

Critical paths are explicitly covered:

- `App` model methods (`docs_filename`, `doc_url`, `get_absolute_url`)
- `app_list` view, full-page and HTMX partial responses
- `app_detail` view, valid and invalid slugs
- `active_link` and `doc_url` template tags
- URL resolver — all named routes
- `seed_apps` management command — create and update paths

See [`docs/SPEC.md` § 18](docs/SPEC.md#18-testing-strategy) for the complete test plan.

---

## Deployment

The site is hosted on Railway with PostgreSQL as the production database. Deploys are triggered automatically when CI passes on `main`.

### One-time setup (already complete)

A new Railway project was created from this GitHub repository. PostgreSQL was added as a service; Railway provides `DATABASE_URL` automatically. Required environment variables:

| Variable | Example | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `core.settings.prod` | Selects production settings |
| `SECRET_KEY` | (50+ random chars) | Django secret |
| `DATABASE_URL` | (auto-injected) | Provided by Railway PostgreSQL service |
| `ALLOWED_HOSTS` | `princetonafeez.com,www.princetonafeez.com` | Comma-separated |
| `DEBUG` | `False` | Never `True` in prod |
| `SENTRY_DSN` | (from sentry.io) | Error monitoring |
| `ADMIN_URL_PREFIX` | `control-9aB4xQ` | Randomized admin URL segment |

Build command:

```bash
pip install -r requirements/prod.txt && \
python manage.py collectstatic --noinput && \
python manage.py migrate && \
python manage.py seed_apps
```

Start command:

```bash
gunicorn core.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

### DNS at GoDaddy

The domain `princetonafeez.com` is registered at GoDaddy. DNS records point at Railway:

- **A** at apex (`@`) → Railway's IPv4 (or CNAME flattening if Railway provides only a hostname)
- **CNAME** for `www` → Railway's provided hostname

HTTPS certificates are issued and renewed automatically by Railway. The certificate covers both the apex and `www`.

Why Railway and not GoDaddy hosting: see [ADR-0002](docs/adr/0002-postgres-on-railway.md).

### Manual deploy (rarely needed)

CI handles all production deploys. To force a redeploy without a code change, push an empty commit:

```bash
git commit --allow-empty -m "Redeploy"
git push
```

---

## Adding an app to the catalogue

The catalogue is driven by [`content/apps.yaml`](content/apps.yaml). To add a new app:

1. **Open** `content/apps.yaml`.
2. **Add a new entry** at the bottom of the `apps:` list. The `build_order` must be unique and is conventionally the next integer after the highest existing one.
3. **Run** `python manage.py seed_apps` to update your local database.
4. **Verify** the new app appears at the top of `/apps/` (reverse-chronological by `build_order`).
5. **Commit** the YAML change. Deploys auto-trigger from `main`.

Entry format:

```yaml
- name: CSV Cleaner
  slug: csv-cleaner
  short_description: "Removes duplicates, normalizes columns, fixes encoding"
  status: completed                   # completed | in_progress | planned
  build_order: 41
  github_url: https://github.com/PrincetonAfeez/Csv-Cleaner
  completed_date: 2026-03-12
  stack: [python, click, pandas]      # references by slug; auto-created on first use
  concepts: [data-cleaning, csv-parsing, cli-design]
```

The `stack` and `concepts` arrays reference `Stack` and `Concept` rows by slug. New slugs are created automatically on first use; existing slugs are linked.

**Documentation convention.** Every app in the catalogue is expected to have a single Markdown documentation file in its own GitHub repository, at the repo root, named in lowercase snake_case with the suffix `_docs.md`. For example, the `String-Sanitizer` repository contains `string_sanitizer_docs.md`. Inside the file, five H2 headings demarcate the five doc sections:

```markdown
# String Sanitizer Documentation

## ADR
...
## TDD
...
## IDS
...
## Runbook
...
## Lessons Learned
...
```

The site renders five buttons on each app's detail page, each deep-linking to the relevant H2 anchor on GitHub. See [ADR-0003](docs/adr/0003-five-docs-via-github-deep-links.md) for the full rationale.

---

## Documentation index

| Document | Purpose |
|---|---|
| [`README.md`](README.md) | This file — orientation, setup, workflow |
| [`docs/SPEC.md`](docs/SPEC.md) | Full v1 specification: positioning, architecture, content plan, security, accessibility |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records (seven for v1) |
| [`SECURITY.md`](SECURITY.md) | Security disclosure contact |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution guidelines (primarily for future-Princeton) |
| [`content/apps.yaml`](content/apps.yaml) | Canonical apps catalogue manifest |

The ADRs cover:

- [0001 — Django + HTMX monolith](docs/adr/0001-django-htmx-monolith.md)
- [0002 — PostgreSQL on Railway](docs/adr/0002-postgres-on-railway.md)
- [0003 — Five docs via GitHub deep links](docs/adr/0003-five-docs-via-github-deep-links.md)
- [0004 — M2M for Stack and Concept](docs/adr/0004-m2m-stack-and-concept.md)
- [0005 — HTMX infinite scroll with pagination fallback](docs/adr/0005-htmx-infinite-scroll.md)
- [0006 — Logging strategy](docs/adr/0006-logging-strategy.md)
- [0007 — Content sync via manifest](docs/adr/0007-content-sync-via-manifest.md)

---

## Roadmap

### v1 (current scope)

- Operator-first home page with work history, capabilities, and certifications
- Apps catalogue with reverse-chronological list, HTMX infinite scroll, progressive-enhancement pagination fallback
- App detail pages with five deep-linked doc buttons
- Contact via `mailto:` and LinkedIn
- Production-grade hardening: security headers, CSP, HSTS, JSON logging, Sentry, 70% test coverage, CI/CD
- WCAG 2.1 AA accessibility target
- Deployed to Railway at `princetonafeez.com` with HTTPS

### v1.1 — Hardening

- Replace Tailwind Play CDN with a compiled Tailwind build; remove `'unsafe-inline'` from `style-src` in the CSP
- Filter chips on `/apps/` — by stack, by status
- Server-side search on `/apps/`

### v1.5 — Operational maturity

- Containerize (Dockerfile + docker-compose for local dev)
- Add a writing section at `/writing/` for technical notes beyond the apps catalogue
- Privacy-respecting analytics (Plausible or Fathom)

### v2 — Extension

- Render the five-doc Markdown directly on-site via a sync command
- RSS feed for new apps
- Dark mode

The full roadmap is in [`docs/SPEC.md` § 24](docs/SPEC.md#24-roadmap).

---

## License

MIT License. See [`LICENSE`](LICENSE) for the full text.

The content of the site (work history, biography, app descriptions, documentation) is © Princeton Afeez and is not covered by the MIT license. The MIT license covers the source code only.

---

## Contact

**Princeton Afeez** — Senior General Manager, Los Angeles
**Email:** [princetonafeez@gmail.com](mailto:princetonafeez@gmail.com)
**LinkedIn:** [linkedin.com/in/princeton-afeez](https://www.linkedin.com/in/princeton-afeez)
**GitHub:** [github.com/PrincetonAfeez](https://github.com/PrincetonAfeez)
**Live site:** [princetonafeez.com](https://princetonafeez.com)
