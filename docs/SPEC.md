# Princeton Afeez Portfolio — Project Specification

**Project:** Personal portfolio capstone documenting Python and system architecture work, anchored by a 35-year hospitality career.
**Domain:** princetonafeez.com (registered at GoDaddy, hosted on Railway)
**Stack:** Python 3.12 · Django 5 · HTMX · PostgreSQL 16 · Tailwind CSS (compiled)
**Status:** v1 specification — locked
**Author:** Princeton Afeez
**Last updated:** May 12, 2026

---

## 1. Overview

This document specifies the design and architecture of a personal portfolio website that serves two purposes:

1. **Represent Princeton Afeez professionally** to hospitality decision-makers (recruiters, owners, regional directors) evaluating him for senior GM, Area Manager, and Regional Director opportunities.
2. **Document Princeton's technical journey** — 40 completed CLI applications, 50 planned applications spanning CLI and web — as a public, growing catalog with consistent documentation across every project.

The site is itself a capstone project. It is the first Django + HTMX application Princeton ships to production, and it demonstrates the same trade-off analysis, architectural discipline, and operational maturity that the catalogued apps demonstrate individually. The site is built to production-grade standards: real database, real CI/CD, real observability, real security headers, real accessibility.

**Positioning line:**
> *35 years operating restaurants. 10+ years of multi-unit P&L ownership. Now studying Python and system architecture.*

**Success criteria for v1:**
- Live at `princetonafeez.com` with HTTPS, custom domain, valid certificate.
- All 40 existing apps catalogued with consistent metadata and deep-linked documentation.
- A hospitality decision-maker can land on the home page, understand Princeton's operator credentials in under 30 seconds, and find a way to contact him in one click.
- A technical reader can land on `/apps/`, browse the chronological catalogue, and open any app's five-section documentation in two clicks.
- 70% test coverage floor with all critical paths exercised; actual coverage at v1 launch is 87.9%.
- CI green on every push to `main`. Deploys auto-trigger on merge.

---

## 2. Positioning and Audience

### Primary audience: hospitality decision-makers

Restaurant owners, group operators, regional directors, hospitality recruiters, and private equity operations partners evaluating Princeton for senior General Manager, Multi-Unit GM, Area Manager, and Regional Director roles. This audience cares about quantified P&L outcomes, multi-unit experience, team development records, and operational systems thinking. They are not technical readers and they have short attention spans.

### Secondary audience: technical readers

Senior engineers, technical hiring managers, accelerator reviewers, and fellow self-taught developers who may discover Princeton through the technical portfolio. This audience cares about architectural decisions, documentation discipline, trade-off analysis, and the credibility of a self-taught learning trajectory.

### Why this ordering matters

The site is operator-first by design. The technical work is a credibility-deepening differentiator — "the senior operator who also ships code" — not the headline. Treating the technical work as the headline would put Princeton in competition with junior CS graduates instead of in a category of one. The operator credentials carry the site; the technical work proves the operator thinks in systems.

### Primary call to action

Direct contact for hospitality opportunities. Expressed as a `mailto:` link to `princetonafeez@gmail.com` and a link to LinkedIn. No contact form.

### Secondary call to action

The `/apps/` page — the reverse-chronological catalogue of all built and planned applications. Reached from a clearly-labelled button on the home page ("My journey in Python") and from the primary navigation.

---

## 3. Information Architecture

### Site map

```
/                       Home (operator-first, with hospitality work history)
/apps/                  Reverse-chronological catalogue of apps
/apps/<slug>/           Individual app detail page
/about/                 Long-form bio (optional, only if home page gets too dense)
/contact/               Direct email + LinkedIn + GitHub
/resume.pdf             Direct PDF download of current resume
/404                    Not found
/500                    Server error
/sitemap.xml            Generated sitemap
/robots.txt             Crawler directives
```

### Page-by-page summary

**Home (`/`)**

Operator-first landing page. Sections, in order:

1. **Hero** — name, headshot, positioning line, two CTAs: "Get in touch" (anchors to `#contact`) and "View my technical work" (links to `/apps/`).
2. **About** — 2–3 paragraph bio. Lagos / London / LA arc. 35 years in hospitality, 10+ years of multi-unit P&L ownership. Current chapter: Crawford's Social, while studying Python and system architecture.
3. **Work history** — anchor case studies for the four strongest roles (Crawford's, Lucky Baldwins, Latte Republique, Coffee Attic / Melrose Station). Each one card showing role, venue, dates, scope, and 2–3 quantified outcomes.
4. **Capabilities** — chip grid covering P&L ownership, multi-unit operations, scratch kitchen launches, team development, vendor management, opening teams, compliance.
5. **Operator tech stack** — chips showing Aloha, Toast, SpotOn, Salido, Caterease, Restaurant365, QuickBooks, MS Office Suite, Adobe Photoshop and Dreamweaver.
6. **Certifications and education** — BA Economics and Business Management; ServSafe Food Protection Manager, ServSafe Food Handler, ServSafe Allergens, ServSafe Workplace, ServSafe Alcohol; eTIPS Certification.
7. **The technical chapter** — short section, 2–3 paragraphs, honest framing: "After 35 years operating restaurants, I'm now studying Python and system architecture. I build small applications to understand how operators' tools actually work underneath. Every project ships with five documents — an ADR, technical design, interface specification, runbook, and lessons learned — because the discipline of writing them is the point." Link to `/apps/`.
8. **Contact** — email, LinkedIn, GitHub. Three icons, no form.
9. **Footer** — copyright, version, link to ADRs.

**Apps catalogue (`/apps/`)**

Reverse-chronological list of every app, newest at top, `string_sanitizer.py` (app #1) at the bottom. Each entry is a card showing:

- App name and build number (e.g., "App #42 of 90")
- Short description (one line)
- Status badge (Completed / In Progress / Planned)
- Stack chips (e.g., Python, Click, pytest)
- "View details" link to `/apps/<slug>/`

HTMX infinite scroll loads 10 apps at a time. Graceful fallback to query-param pagination if JavaScript is disabled.

**App detail (`/apps/<slug>/`)**

Per-app deep-dive page:

- Hero image (optional)
- App name, build order, status
- Short description
- Stack chips and concept chips
- "View on GitHub" primary button
- Five "Documentation" buttons, each deep-linking to the relevant H2 anchor in the app's single Markdown documentation file on GitHub:
  - 📄 ADR
  - 📐 TDD (Technical Design Document)
  - 🔌 IDS (Interface Design Specification)
  - 📖 Runbook
  - 🎓 Lessons Learned
- "Back to all apps" link

**Contact (`/contact/`)**

Three rows: direct email (`mailto:princetonafeez@gmail.com`), LinkedIn URL, GitHub URL. No form.

**404 and 500**

Custom branded templates. 404 offers a link home and to `/apps/`. 500 is minimal and does not extend the marketing layout (in case the layout itself is what failed).

---

## 4. Content Plan

### Hero copy

> # Princeton Afeez
>
> ## 35 years operating restaurants. 10+ years of multi-unit P&L ownership.
>
> Senior General Manager · Los Angeles · Currently at Crawford's Social
>
> Every role inherited a problem. Every role left behind a system.

### About copy (draft)

> I've spent 35 years in hospitality, the last 10+ as a multi-unit General Manager running full-service restaurants, cafés, lounges, and high-volume catering across Los Angeles. I've managed up to five locations simultaneously, 85+ employees, and 8-figure annual revenue. I've reduced food cost by up to 15 points, compressed labor by 17 points, launched scratch kitchen programs from zero, and built management teams that drove 10% year-over-year revenue growth.
>
> I'm currently the Interim General Manager at Crawford's Social — a 430-seat full-service New American restaurant and craft cocktail bar in Los Angeles.
>
> Outside of hospitality, I'm in the middle of a long-form study of Python and system architecture. I build small applications, document them rigorously, and publish them here. The discipline is the point.

### Work history items

Four hero case studies on the home page. Each one card. Sourced from the resume.

**1. Crawford's Social — Interim General Manager (Oct 2025 – Present)**

> 430-seat full-service New American restaurant and craft cocktail bar. 8-figure annual revenue, 80+ staff. Redesigned FOH service flow and floor rotation, increasing covers per service during peak volume. Built a 5-manager development program with zero turnover during engagement. Passed health, safety, and liquor compliance audits with zero violations.

**2. Lucky Baldwins — Multi-Unit General Manager (Apr 2021 – Sep 2025)**

> Three-location British pub group. Full P&L ownership, 8-figure annual revenue. Cut food cost 15 points (40% → 25%) and labor cost 17 points (45% → 28%) — the largest margin improvement in the brand's history. Aligned all three units around unified SOPs, financial targets, and guest service standards through aggressive post-pandemic recovery.

**3. Latte Republique — Multi-Unit General Manager (Aug 2012 – Jun 2017)**

> Five French-American breakfast cafés. 85+ employees: 5 GMs, 5 AGMs, 25 cooks, 50 baristas. Full P&L ownership. Drove 10% year-over-year sales growth across all five locations. 100% compliance with all local, state, and federal regulations across five years — zero violations, zero fines.

**4. Coffee Attic, Melrose Station & Glass Hookah Lounge — Multi-Concept GM (Jul 2017 – Mar 2020)**

> Three distinct concepts on Melrose Avenue — café, craft cocktail lounge, hookah lounge. Transitioned all kitchens from frozen and pre-packaged to 100% scratch preparation, a first in the brand's history; delivered a 23% food cost reduction through vendor renegotiation. Designed and built a new outdoor patio that grew seating capacity from 60 to 100+.

Additional roles surfaced in a smaller "Earlier roles" list: HabachiHana Grill (4 locations, Jun 2020 – Jan 2021), Garden of Eating (corporate catering, Sep 2019 – Jun 2020), and the additional hospitality experience block from the resume (Fundamental Events, Bardonna Café, Carvery, Fish Trap, Anejo Cantina, Belgo Restaurant, Planet Hollywood, Sound Restaurant, Smolensky's, Capital Radio Café, Sound Republic, Royal House Catering).

### Capabilities chips

Multi-Unit P&L Ownership · Food and Labor Cost Engineering · Scratch Kitchen Launch · Revenue Growth Strategy · Staff Recruitment, Training and Retention · SOP Design and Deployment · Guest Experience Systems · Inventory and Vendor Management · New Unit Opening and Turnaround · Health, Safety and Compliance · BOH/FOH Operations · Facility Expansion · POS and Technology Optimization · Financial Forecasting and Budgeting

### Operator tech stack chips

Aloha · Toast · SpotOn · Salido · Caterease · Restaurant365 · Intuit QuickBooks · Microsoft Office Suite · Adobe Photoshop · Adobe Dreamweaver

### Certifications

ServSafe Food Protection Manager · ServSafe Food Handler · ServSafe Allergens · ServSafe Workplace · ServSafe Alcohol · eTIPS

### Education

Bachelor of Arts in Economics and Business Management

### The technical chapter

> After 35 years operating restaurants, I'm now studying Python and system architecture. I build small applications — most of them command-line tools, some of them web applications — to learn the disciplines that go into shipping software. Every project ships with five documents: an Architecture Decision Record, a Technical Design Document, an Interface Design Specification, a Runbook, and a Lessons Learned retrospective.
>
> The discipline is the point. The applications themselves are small. The catalog of decisions, designs, interfaces, runbooks, and reflections is the artifact.
>
> *[Button: Browse all apps →]*

### Assets

- **Headshot:** committed in the repository at `static/img/headshot.png` (no runtime dependency on the legacy site).
- **Resume:** PDF, served at `/resume.pdf`.

---

## 5. Data Model

The data model is intentionally small. Three models, two many-to-many relationships, no overengineering.

```python
# portfolio/models.py

from django.db import models
from django.urls import reverse


class Stack(models.Model):
    """A technology used in an app: language, framework, library, tool, database, service."""
    CATEGORY_CHOICES = [
        ('language', 'Language'),
        ('framework', 'Framework'),
        ('library', 'Library'),
        ('tool', 'Tool'),
        ('database', 'Database'),
        ('service', 'Service'),
    ]

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Concept(models.Model):
    """A concept or skill demonstrated by an app: e.g., 'string-manipulation', 'rest-apis'."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class App(models.Model):
    """A single app in the portfolio: CLI, web, or hybrid."""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    short_description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    build_order = models.PositiveIntegerField(unique=True, db_index=True)
    github_url = models.URLField()
    docs_url = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to='apps/', blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stack = models.ManyToManyField(Stack, related_name='apps', blank=True)
    concepts = models.ManyToManyField(Concept, related_name='apps', blank=True)

    class Meta:
        ordering = ['-build_order']

    def __str__(self):
        return f"#{self.build_order} {self.name}"

    def get_absolute_url(self):
        return reverse('portfolio:app_detail', kwargs={'slug': self.slug})

    @property
    def docs_filename(self):
        """Derives the docs filename from the app name.

        Convention: lowercase, spaces → underscores, suffix _docs.md, at repo root.
        Example: 'String Sanitizer' → 'string_sanitizer_docs.md'
        """
        return f"{self.name.lower().replace(' ', '_')}_docs.md"

    DOC_ANCHORS = {
        'ADR': 'adr',
        'TDD': 'tdd',
        'IDS': 'ids',
        'RUNBOOK': 'runbook',
        'LESSONS_LEARNED': 'lessons-learned',
    }

    def doc_url(self, doc_type: str) -> str:
        """Constructs the deep-linked GitHub URL for a given doc section.

        Example:
            app.doc_url('ADR')
            → 'https://github.com/PrincetonAfeez/String-Sanitizer/blob/main/string_sanitizer_docs.md#adr'
        """
        anchor = self.DOC_ANCHORS[doc_type]
        docs_url = self.docs_url or f"{self.github_url}/blob/main/{self.docs_filename}"
        return f"{docs_url}#{anchor}"
```

### Notes on the data model

- **The five docs are not stored in the database.** They live in each app's GitHub repository as one Markdown file per app (e.g., `string_sanitizer_docs.md`). The five sections within that file are H2 headings, and the site deep-links to each H2's auto-generated GitHub anchor. See ADR-0003.
- **`github_url` is the visible source link.** `docs_url` is the exact Markdown documentation file URL used for the five documentation buttons. If `docs_url` is blank, the site falls back to the default filename convention under `github_url`.
- **`build_order` is the canonical sort field**, not `completed_date`. This shows progression in the order Princeton actually built the apps, even if he completes them out of order.
- **M2M for `stack` and `concept`** rather than free-text fields. Filtering is out of scope for v1, but the data model supports it without migration. See ADR-0004.
- **Indexes:** `slug` (unique, default index), `build_order` (unique, explicit index for ordering performance).
- **No through-model fields** on the M2Ms in v1. If display ordering of chips ever matters, add a through model with an `order` field.

---

## 6. Technical Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 | Current stable, type-hint maturity, matches Princeton's learning track |
| Web framework | Django 5 | Batteries included, mature ORM, admin, security baseline |
| Interactivity | HTMX (self-hosted UMD under `static/vendor/`) | Server-rendered enhancement, no JS framework, no third-party script origin in CSP |
| Database (prod) | PostgreSQL 16 | Production standard, hosted by Railway |
| Database (dev) | SQLite | Fast local iteration, no setup overhead |
| Styling | Tailwind CSS compiled in v1 (`npm run build:css`, Tailwind 3 JIT) | Strong CSP (`style-src 'self'`), only utilities referenced in templates |
| Icons | Lucide (self-hosted UMD under `static/vendor/`) | Open-source, comprehensive; no third-party script origin in CSP |
| Markdown rendering | Not applicable in v1 | Docs are deep-linked to GitHub, not rendered on-site |
| Static files | WhiteNoise with `CompressedManifestStaticFilesStorage` (prod) | Cache-busting filenames and compression; no separate CDN needed for v1 |
| Application server | Gunicorn | Standard, well-understood, two workers sufficient for v1 traffic |
| Error monitoring | Sentry (free tier, 10% trace sampling, PII off) | Capture unhandled exceptions and 500s in prod |
| Logging | `python-json-logger` (prod) + standard logging (dev) | JSON for log aggregation, human-readable for local |
| Content Security Policy | `django-csp` 4.x (dict-based `CONTENT_SECURITY_POLICY`) | Locked to `'self'`; no inline scripts or third-party CDNs |
| Test runner | pytest + pytest-django | More expressive than unittest, ecosystem better |
| Coverage | `coverage.py` (87.9% at v1 launch, 70% CI floor) | Enforced in CI; uncovered branches are deliberate exclusions |
| Accessibility smoke | Playwright + axe-core | Browser-based a11y checks under `e2e/` |
| Linting | `ruff` | Fast, single tool replaces multiple |
| Formatting | `black` | Standard, opinionated, no debate |
| Template linting | `djlint` | Catches template issues that `ruff` and `black` won't see |
| CI | GitHub Actions | Native integration with the repo |
| Hosting | Railway | Easy Django + Postgres deploys, CI-friendly, custom domain support |
| DNS / Domain | GoDaddy (registrar only) | Pre-existing domain registration, no migration needed |

---

## 7. Project Structure

```
princetonafeez/
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── docs/
│   ├── README.md
│   ├── SPEC.md                              # This document
│   ├── ADRS.md                              # All seven ADRs in one compendium
│   └── notes/                               # Working notes (not part of the published spec)
│       ├── content.txt
│       ├── project-tree.txt
│       └── technical docs.txt
├── manage.py
├── pyproject.toml
├── package.json                             # Tailwind build scripts (`npm run build:css`)
├── package-lock.json
├── tailwind.config.cjs
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── VERSION
├── railway.toml
├── content/
│   ├── README.md
│   └── apps.yaml                            # Manifest: all 90 apps, version-controlled
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── context_processors.py
│   ├── logging_config.py
│   ├── middleware.py                        # AdminIPAllowlistMiddleware (prod admin IP gate)
│   ├── sitemaps.py                          # Sitemap classes for django.contrib.sitemaps
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── test.py
│   │   └── prod.py
│   └── tests/
│       ├── __init__.py
│       ├── test_context_processors.py
│       ├── test_middleware.py
│       └── test_prod_settings.py
├── e2e/
│   ├── __init__.py
│   ├── conftest.py
│   ├── axe_helpers.py
│   └── test_smoke_a11y.py                   # Playwright + axe smoke accessibility checks
├── static/
│   ├── css/
│   │   ├── tw-input.css                     # Tailwind source (JIT entry)
│   │   ├── tw-compiled.css                  # Built bundle (committed; CI/deploy rebuilds)
│   │   └── site.css                         # Project overrides and tokens
│   ├── js/
│   │   └── icons-init.js                    # Lucide `createIcons()` after load
│   ├── img/
│   │   ├── README.md
│   │   └── headshot.png
│   ├── vendor/
│   │   ├── htmx.min.js
│   │   └── lucide.min.js
│   └── resume/
│       ├── README.md
│       └── resume.pdf                       # Served at /resume.pdf (see URL routing)
├── pages/
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   ├── content.py                           # NAV_ITEMS, FOOTER_LINKS, SITE_NAME etc.
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── nav_tags.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_views.py
│   │   └── test_template_tags.py
│   └── templates/
│       ├── base.html
│       ├── 404.html
│       ├── 500.html
│       ├── layouts/
│       │   └── default.html
│       ├── pages/
│       │   ├── home.html
│       │   ├── about.html
│       │   └── contact.html
│       ├── components/
│       │   ├── navbar.html
│       │   ├── footer.html
│       │   ├── status_badge.html
│       │   ├── case_study_card.html
│       │   └── chip.html
│       └── sections/
│           ├── hero.html
│           ├── about.html
│           ├── work_history.html
│           ├── capabilities.html
│           ├── certifications.html
│           ├── tech_chapter.html
│           └── contact.html
└── portfolio/
    ├── __init__.py
    ├── apps.py
    ├── admin.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── templatetags/
    │   ├── __init__.py
    │   └── doc_tags.py
    ├── management/
    │   └── commands/
    │       └── seed_apps.py
    ├── migrations/
    ├── tests/
    │   ├── __init__.py
    │   ├── test_models.py
    │   ├── test_views.py
    │   ├── test_urls.py
    │   ├── test_template_tags.py
    │   └── test_seed_apps.py
    └── templates/
        └── portfolio/
            ├── app_list.html
            ├── app_detail.html
            └── partials/
                ├── app_card.html
                └── app_list_page.html
```

Two Django apps: `pages` (the static marketing surface — home, about, contact, error pages, components) and `portfolio` (the dynamic catalogue — App model, list view, detail view, seed command). Clean separation of concerns. Each app has its own tests directory. The `core` package adds URL routing, context processors, logging configuration, `AdminIPAllowlistMiddleware` and sitemap classes (`middleware.py`, `sitemaps.py`), settings split, and `core/tests/` for those concerns. First-party static assets and the Tailwind build artifacts live under `static/`; Node dependencies and `npm run build:css` are declared in `package.json` / `package-lock.json`. Optional Playwright + axe smoke checks live under `e2e/`.

---

## 8. Settings Split

Four settings files. Selected at runtime by `DJANGO_SETTINGS_MODULE`.

### `core/settings/base.py`

Shared defaults: `INSTALLED_APPS`, `MIDDLEWARE`, `TEMPLATES` (with the site context processor wired in), `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT`, the security middleware baseline, the `LOGGING` configuration loaded via `core.logging_config.build_logging_config()`, and any other concerns that apply to every environment.

### `core/settings/dev.py`

`DEBUG = True`, `ALLOWED_HOSTS = ['*']`, SQLite database, console-only logging with the human-readable formatter, Django Debug Toolbar enabled, no SSL redirects. Content Security Policy is enforced in production only (`django-csp` in `prod.py`); local dev does not load the CSP middleware, which keeps the Django Debug Toolbar usable without CSP exceptions.

### `core/settings/test.py`

Imports everything from `core/settings/base.py` and applies a small set of overrides — nothing from `prod.py` is merged in.

- **`DEBUG = False`** — matches production's debug flag without enabling prod-only middleware or storage.
- **`PASSWORD_HASHERS`** — `MD5PasswordHasher` only, for faster tests (this module must not be used for `runserver` or production; see the module docstring).
- **`EMAIL_BACKEND`** — `django.core.mail.backends.locmem.EmailBackend` so tests never send real mail.
- **`DATABASES`** — if `DATABASE_URL` is set, the default database is replaced with PostgreSQL via `dj_database_url` (`conn_max_age=0`). If it is unset, the configuration **keeps SQLite from `base.py`**. CI sets `DATABASE_URL` so the pipeline exercises PostgreSQL; a developer can run pytest locally without Postgres and still use SQLite.
- **`LOGGING`** — `build_logging_config(is_prod=False)`, i.e. the same **development-style** (human-readable console) logging as `base.py` / `dev.py`, not the JSON production formatter.

Templates, `STATIC_URL` / `STATIC_ROOT` / `STATICFILES_DIRS`, and the default staticfiles backend therefore stay exactly as in **`base.py`**. Test settings do **not** enable production-only `STORAGES` (`CompressedManifestStaticFilesStorage`), `django-csp`, or other `prod.py` security and static-asset behavior — those exist only under `core.settings.prod`.

### `core/settings/prod.py`

`DEBUG = False`, `ALLOWED_HOSTS` from environment, PostgreSQL via `DATABASE_URL`, console-only logging with the JSON formatter (Railway captures stdout for log aggregation, no file handler needed), strict CSP, full security headers, `SECURE_SSL_REDIRECT = True`, `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`, HSTS, Sentry SDK initialized.

### Required environment variables

| Variable | Used in | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | All | `core.settings.dev`, `core.settings.test`, or `core.settings.prod` |
| `SECRET_KEY` | All | Django secret. 50+ random chars. |
| `DATABASE_URL` | Test, Prod | CI service URL in tests; provided by Railway PostgreSQL service in prod |
| `ALLOWED_HOSTS` | Prod | Comma-separated: `princetonafeez.com,www.princetonafeez.com` |
| `CSRF_TRUSTED_ORIGINS` | Prod | Comma-separated with scheme: `https://princetonafeez.com,https://www.princetonafeez.com` |
| `ADMIN_URL_PREFIX` | Prod | Randomized admin path segment, e.g. `control-9aB4xQ` |
| `ADMIN_ALLOWED_IPS` | Prod | **Required** in production: comma-separated IPs allowed to reach Django admin (empty or unset raises `ImproperlyConfigured`). |
| `SENTRY_DSN` | Prod | Sentry project DSN |
| `DEBUG` | All | `True` or `False` |

A `.env.example` ships with the repo documenting every variable. Local dev uses a `.env` file (gitignored), loaded by the project's small in-process dotenv helper in `core/settings/base.py`.

---

## 9. URL Routing

All URLs are namespaced.

```python
# core/urls.py (representative; matches shipped handlers and main routes)
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import AppSitemap, StaticViewSitemap
from pages import views as page_views

sitemaps = {"static": StaticViewSitemap, "apps": AppSitemap}

urlpatterns = [
    path(f"{settings.ADMIN_URL_PREFIX.strip('/')}/", admin.site.urls),
    path("", include(("pages.urls", "pages"), namespace="pages")),
    path("apps/", include(("portfolio.urls", "portfolio"), namespace="portfolio")),
    path("resume.pdf", page_views.resume_pdf, name="resume_pdf"),
    path("robots.txt", page_views.robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
```

```python
# pages/urls.py
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
```

```python
# portfolio/urls.py
urlpatterns = [
    path('', views.app_list, name='app_list'),
    path('<slug:slug>/', views.app_detail, name='app_detail'),
]
```

---

## 10. Templates and Components

### Three-level inheritance

```
base.html
  └── layouts/default.html
        ├── pages/home.html
        ├── pages/about.html
        ├── pages/contact.html
        ├── portfolio/app_list.html
        └── portfolio/app_detail.html
```

`base.html` defines the document skeleton: `<html>`, `<head>` with named blocks for title, meta description, OG tags, Twitter card, canonical URL; loads compiled Tailwind (`tw-compiled.css`) plus project CSS (`site.css`); loads HTMX and Lucide as self-hosted scripts from `static/vendor/` and a small `icons-init.js`; defines CSS custom properties for design tokens; opens a single `{% block content %}` and `{% block scripts %}`.

`layouts/default.html` extends `base.html`, includes the navbar and footer components, wraps `{% block page_content %}` in the marketing-page container styling.

Page templates extend `layouts/default.html` and fill `{% block page_content %}`.

### Components (includes)

| Component | Purpose | Variables |
|---|---|---|
| `navbar.html` | Top navigation | Uses `NAV_ITEMS` from context |
| `footer.html` | Footer with links and version | Uses context processor values |
| `status_badge.html` | App status pill | `status` |
| `case_study_card.html` | Work history card on home | `case_study` (dataclass) |
| `chip.html` | Capability / stack / concept chip | `label`, `variant` |
| `app_card.html` (portfolio) | App card on `/apps/` | `app` (App instance) |

### Sections (partials, included into pages)

| Section | Used on |
|---|---|
| `hero.html` | Home |
| `about.html` | Home |
| `work_history.html` | Home |
| `capabilities.html` | Home |
| `certifications.html` | Home |
| `tech_chapter.html` | Home |
| `contact.html` | Home, Contact |

### Custom template tags

Two tags, no filters.

**`{% active_link 'pages:home' %}`** (in `pages/templatetags/nav_tags.py`)

Returns the CSS class `"active"` (mapped in styles to bold + accent color) when the current request path matches the named URL, empty string otherwise. Implemented as a `simple_tag(takes_context=True)`.

**`{% doc_url app 'ADR' %}`** (in `portfolio/templatetags/doc_tags.py`)

Thin wrapper around `App.doc_url()` so templates can call the method with an argument. Returns the deep-linked GitHub URL for the named doc section.

---

## 11. HTMX Infinite Scroll Architecture

The apps catalogue at `/apps/` uses HTMX-driven infinite scroll, with graceful degradation to traditional pagination if JavaScript is disabled. This is documented in ADR-0005.

### Server-side

A single view handles both the full-page and partial responses:

```python
# portfolio/views.py
from django.core.paginator import Paginator
from django.shortcuts import render

PAGE_SIZE = 10


def app_list(request):
    page_number = int(request.GET.get('page', 1))
    apps_qs = App.objects.prefetch_related('stack', 'concepts').order_by('-build_order')
    paginator = Paginator(apps_qs, PAGE_SIZE)
    page = paginator.get_page(page_number)

    context = {
        'apps': page.object_list,
        'page': page,
        'has_next': page.has_next(),
        'next_page': page.next_page_number() if page.has_next() else None,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'portfolio/partials/app_list_page.html', context)
    return render(request, 'portfolio/app_list.html', context)
```

### Client-side pattern

The template emits 10 app cards. After the last card, an HTMX trigger element renders:

```html
{% if has_next %}
  <div
    hx-get="{% url 'portfolio:app_list' %}?page={{ next_page }}"
    hx-trigger="revealed"
    hx-swap="outerHTML"
    class="htmx-trigger">
    <noscript>
      <a href="?page={{ next_page }}" class="pagination-fallback">Load more</a>
    </noscript>
  </div>
{% endif %}
```

When the trigger element enters the viewport, HTMX fires `hx-get`, the server returns the next 10 cards plus a new trigger element, HTMX swaps the old trigger for the new content. The cycle repeats until there's no next page.

If JavaScript is disabled, the `<noscript>` fallback renders a real anchor link that loads `?page=2` as a full page navigation. The same view handles both paths.

### Accessibility

The HTMX-loaded content is announced to assistive technologies via an `aria-live="polite"` region wrapping the app list, so screen reader users hear new cards as they load. A regression test in `portfolio/tests/test_views.py` asserts the presence of `id="app-list"` and `aria-live="polite"` on the catalogue page, so the contract is enforced by CI.

---

## 12. App Documentation Linking

This is the key architectural pattern for the technical-portfolio half of the site. Documented in ADR-0003.

### Convention

Each app in Princeton's GitHub has a single Markdown documentation file. The exact file URL is stored in `content/apps.yaml` as `docs_url` so the site does not have to infer paths for monorepo or renamed repositories. Most files follow the lowercase snake_case suffix convention:

```
github.com/PrincetonAfeez/String-Sanitizer/blob/main/string_sanitizer_docs.md
github.com/PrincetonAfeez/Csv-Cleaner/blob/main/csv_cleaner_docs.md
```

Inside each documentation file, five H2 headings demarcate the five doc sections:

```markdown
# String Sanitizer Documentation

## ADR

[Architecture Decision Record content here]

## TDD

[Technical Design Document content here]

## IDS

[Interface Design Specification content here]

## Runbook

[Runbook content here]

## Lessons Learned

[Lessons Learned content here]
```

### Why H2 and not H1

H1 is reserved for the document title. Multiple H1s in a single document break semantic structure and confuse screen readers and GitHub's rendering. H2 for each section gives a clean hierarchy and predictable anchor generation. See ADR-0003 for the full rationale.

### Site rendering

The app detail page renders five buttons. Each button is constructed via the `doc_url` template tag, which calls `App.doc_url(doc_type)`. The returned URL deep-links to the relevant H2 anchor on GitHub:

```
{docs_url}#{anchor}
```

Where `docs_url` is the exact Markdown file URL stored in the manifest, and `anchor` comes from the `App.DOC_ANCHORS` mapping (e.g., `'LESSONS_LEARNED' → 'lessons-learned'`). If a legacy row does not have `docs_url`, the model falls back to `{github_url}/blob/main/{docs_filename}#{anchor}`.

### Source of truth

The Markdown files themselves remain in each app's GitHub repository. The portfolio site **does not duplicate** their content; it only links to it. This keeps the portfolio site lightweight, ensures the docs stay co-located with their code, and avoids a content-sync problem where the site's copy diverges from the canonical copy.

---

## 13. Security

### Middleware-level headers

Configured in `core/settings/base.py` and tightened in `prod.py`:

```python
# In base.py (apply everywhere)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# In prod.py only (require HTTPS context)
SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Content Security Policy

Via `django-csp` 4.x (`CONTENT_SECURITY_POLICY` dict). `csp` is appended to `INSTALLED_APPS` and `CSPMiddleware` is inserted **after** `WhiteNoiseMiddleware` in `prod.py` (following django-csp guidance) so responses that pass through both middlewares get CSP headers consistently — including any HTML inadvertently served via the static pipeline. This is additional defense-in-depth, not a claim that typical static files need CSP: most WhiteNoise responses are non-HTML assets, and CSP primarily governs HTML documents. Configured in `prod.py`:

```python
from csp.constants import NONE, SELF

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [SELF],
        "style-src": [SELF],
        "img-src": [
            SELF,
            "data:",
            "https://github.com",
            "https://avatars.githubusercontent.com",
        ],
        "font-src": [SELF, "data:"],
        "connect-src": [SELF],
        "frame-ancestors": [NONE],
        "base-uri": [SELF],
        "form-action": [SELF],
    },
}
```

Scripts and styles are limited to first-party static files: compiled Tailwind + `site.css`, and self-hosted HTMX / Lucide. The Tailwind Play CDN and a broad `style-src 'unsafe-inline'` allowance are not used. See ADR-0001.

### Admin protection

Django admin is enabled for content edits but is not the primary content workflow. The seed manifest is. To minimize admin exposure:

- Superuser credentials are strong (16+ char password, env-derived).
- The admin URL is not the default `/admin/` — it is randomized via env (e.g., `/control-9aB4xQ/`) and documented in `.env.example` as a configuration value.
- An IP allowlist middleware (`AdminIPAllowlistMiddleware` in `core/middleware.py`) restricts admin access to Princeton's known IP addresses; non-allowlisted requests to admin URLs return 404. Production settings require a non-empty `ADMIN_ALLOWED_IPS` (startup fails with `ImproperlyConfigured` if unset or empty); a regression test in `core/tests/test_prod_settings.py` exercises this contract.

### Forms

There are no user-input forms in v1. Contact is `mailto:` only. This eliminates an entire class of attack surface (spam, injection, CSRF on submitted forms, file uploads). Documented in ADR-0001.

---

## 14. Logging and Observability

### Structure

`core/logging_config.py` exports a single function:

```python
def build_logging_config(is_prod: bool) -> dict:
    """Returns the Django LOGGING dict for the current environment."""
```

Called from `base.py` with `IS_PROD` from environment.

### Dev configuration

- Single console handler.
- Human-readable formatter: `%(asctime)s %(levelname)-8s %(name)s %(message)s`.
- Level: `DEBUG` for `portfolio` and `pages` loggers; `INFO` for Django.

### Prod configuration

- Single console handler (Railway captures stdout for its log aggregation).
- JSON formatter via `python-json-logger`: emits `timestamp`, `level`, `logger`, `message`, `module`, `funcName`, `lineno`, `pathname`.
- Level: `INFO` for application loggers; `WARNING` for Django.

### Why this split

Local terminals render human-readable text well. Log aggregators (Datadog, Loki, CloudWatch, Railway's built-in logs) parse structured JSON well. Forcing one format on both environments breaks the use case it isn't designed for. See ADR-0006.

### Error monitoring

Sentry SDK initialized in `prod.py` only. Captures unhandled exceptions, 500-level responses, and a 10% sample of performance traces (`traces_sample_rate=0.1`, `send_default_pii=False`). DSN from env. Free tier sufficient for portfolio traffic.

---

## 15. Performance

### Targets

- Home page Largest Contentful Paint < 1.5s on 4G mobile (Chrome Lighthouse mobile profile).
- Apps catalogue first paint < 1.5s; HTMX append for next batch < 300ms.
- App detail page < 1.0s LCP.

### Tactics

- **Database query optimization:** `App.objects.prefetch_related('stack', 'concepts')` on the catalogue view to eliminate N+1 queries.
- **Static file serving:** WhiteNoise with `CompressedManifestStaticFilesStorage` for cache-busting filenames and gzip/brotli compression.
- **Image optimization:** all hero images converted to WebP with JPEG fallback via `<picture>`. All images carry `loading="lazy"` except the home page hero.
- **HTMX over full-page navs:** the apps catalogue loads more content without a full page reload, reducing repeat asset downloads.
- **No client-side framework:** zero JavaScript bundle beyond HTMX (~14KB gzipped).
- **Compiled Tailwind in v1:** Tailwind 3 JIT scans Django templates and emits `tw-compiled.css`; content-hashed via WhiteNoise manifest storage in production.

---

## 16. Accessibility

Target: WCAG 2.1 Level AA.

### Structural

- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`.
- Single `<h1>` per page (the page title).
- Logical heading hierarchy. No skipped levels.
- Skip-to-content link as the first focusable element on every page.
- Mobile navigation uses the native `<details>`/`<summary>` element — no JavaScript required.

### Interactive

- All interactive elements reachable by keyboard.
- Visible focus styles on every focusable element (custom focus ring on `:focus-visible`).
- Buttons and links have accessible names. Icon-only buttons carry `aria-label`.
- The HTMX-loaded app catalogue uses an `aria-live="polite"` region so new cards are announced. A unit test asserts this region's presence and attributes; an `e2e/` Playwright + axe smoke test covers a broader set of page-level a11y checks.

### Visual

- Color contrast for body text ≥ 4.5:1.
- Color contrast for large text and UI components ≥ 3:1.
- No information conveyed by color alone (status badges use both color and text label).
- Text resizable to 200% without loss of content or function.

### Images

- Every meaningful image has descriptive `alt` text.
- Decorative images carry `alt=""`.

---

## 17. SEO

### Page-level metadata

Every page sets:

- `<title>` — concise, page-specific, includes site name
- `<meta name="description">` — 140–160 characters
- `<link rel="canonical">` — full absolute URL
- Open Graph tags: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`
- Twitter Card tags: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`

Implemented via named template blocks: `{% block title %}`, `{% block meta_description %}`, `{% block og_image %}`, etc.

### Structured data (JSON-LD)

- Home page: `Person` schema (name, jobTitle, address, sameAs links to LinkedIn/GitHub).
- App detail pages: `SoftwareApplication` schema (name, applicationCategory, description, url, dateCreated).

### Sitemap

Sitemap classes live in `core/sitemaps.py` and are exposed via `core/urls.py` using `django.contrib.sitemaps`, with entries for: home, about, contact, every app detail page. Updated automatically when apps are added via the seed command.

### Robots

`/robots.txt` allows all crawlers. No paid private content to hide. Excludes the admin URL.

---

## 18. Testing Strategy

### Framework

`pytest` + `pytest-django` + `pytest-cov`. Tests live under `<app>/tests/`. Browser-based accessibility smoke checks live under `e2e/` using Playwright + axe-core.

### Coverage

70% line coverage minimum, enforced in CI. The build fails if coverage drops below that threshold. **Actual coverage at v1 launch is 87.9%**, with deliberate exclusions for:

- Environment-specific settings files (`core/settings/dev.py`, `core/settings/prod.py`) — testing them would mostly re-assert literal values and provide false confidence.
- WSGI/ASGI entrypoints (`core/wsgi.py`, `core/asgi.py`) and `manage.py` — Django boilerplate, tested upstream.
- A handful of defensive error branches in middleware and 500 handler — fire on conditions that are hard to construct without contortion.

The 70% floor is the safety net; 87.9% is the actual quality bar maintained by the test suite. New code that drops the number toward 70% should justify the dip in the same PR.

### Critical paths (must be covered)

| Component | Test |
|---|---|
| `App.docs_filename` | Returns correct snake_case `_docs.md` for various names |
| `App.doc_url('ADR')` | Returns correct deep-linked URL for each doc type |
| `App.doc_url('INVALID')` | Raises KeyError |
| `App.get_absolute_url` | Returns the correct detail page URL |
| `app_list` view | 200 on full page request |
| `app_list` view (HX-Request) | Returns partial template with correct content |
| `app_list` view pagination | `?page=2` returns the right 10 apps |
| `app_list` accessibility | `id="app-list"` and `aria-live="polite"` present on the list |
| `app_detail` view | 200 for existing slug |
| `app_detail` view | 404 for missing slug |
| `home` view | 200, contains positioning line |
| `contact` view | 200, contains email link |
| `active_link` template tag | Returns "active" for current path, empty otherwise |
| `doc_url` template tag | Wraps `App.doc_url` correctly |
| `seed_apps` command | Creates new apps from manifest |
| `seed_apps` command | Updates existing apps idempotently |
| `core.settings.prod` | Raises `ImproperlyConfigured` when `ADMIN_ALLOWED_IPS` is empty |
| `AdminIPAllowlistMiddleware` | Returns 404 for non-allowlisted IPs hitting admin |
| URL resolver | All named routes resolve |
| 404 handler | Custom template renders |
| 500 handler | Custom template renders |

### Out of scope for tests

- Exhaustive template rendering — covered by the view tests at the smoke-test level.
- Django admin — uses Django's built-in admin; tested upstream.
- Third-party middleware (`django-csp`, `whitenoise`) — tested upstream.

---

## 19. CI/CD

### Workflow file

`.github/workflows/ci.yml` runs on every push and pull request to `main`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - name: Install dependencies
        run: pip install -r requirements/dev.txt
      - name: Lint with ruff
        run: ruff check .
      - name: Check format with black
        run: black --check .
      - name: Lint templates with djlint
        run: djlint pages/templates portfolio/templates --check
      - name: Run migrations
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
          DJANGO_SETTINGS_MODULE: core.settings.test
        run: python manage.py migrate
      - name: Run tests with coverage
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
          DJANGO_SETTINGS_MODULE: core.settings.test
        run: pytest --cov=. --cov-fail-under=70
```

### Deployment

Railway auto-deploys from `main` when CI passes. The build command runs **`npm ci`** and **`npm run build:css`** (Tailwind → `static/css/tw-compiled.css`), then `pip install`, `collectstatic`, `migrate`, and `seed_apps` — matching `railway.toml`. The start command runs `gunicorn`.

---

## 20. Deployment

### Railway setup

1. New project from the GitHub repo.
2. Add the PostgreSQL plugin. Railway provides `DATABASE_URL` automatically.
3. Set environment variables:
   - `DJANGO_SETTINGS_MODULE = core.settings.prod`
   - `SECRET_KEY = <generated, 50+ chars>`
   - `ALLOWED_HOSTS = princetonafeez.com,www.princetonafeez.com`
   - `CSRF_TRUSTED_ORIGINS = https://princetonafeez.com,https://www.princetonafeez.com`
   - `DEBUG = False`
   - `SENTRY_DSN = <from Sentry>`
   - `ADMIN_URL_PREFIX = control-<random>`
   - `ADMIN_ALLOWED_IPS = <comma-separated IPs>` — **required** in production; startup fails if unset or empty (see §8 and `core/settings/prod.py`).
4. Build command (same sequence as [`railway.toml`](../railway.toml) `buildCommand`; Nixpacks must have Node available for `npm`):
   ```
   npm ci && npm run build:css && \
   pip install -r requirements/prod.txt && \
   python manage.py collectstatic --noinput && \
   python manage.py migrate && \
   python manage.py seed_apps
   ```
5. Start command:
   ```
   gunicorn core.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
   ```
6. Custom domains: add `princetonafeez.com` and `www.princetonafeez.com`. Railway provides the target hostname.

### Pre-deploy local rehearsal

Before pushing changes that affect static assets or settings, rehearse the production pipeline locally:

```bash
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))") \
  ALLOWED_HOSTS=localhost \
  ADMIN_ALLOWED_IPS=127.0.0.1 \
  DATABASE_URL=postgresql://localhost/portfolio_local \
  python manage.py collectstatic --noinput
```

This exercises `CompressedManifestStaticFilesStorage` locally. Any template that references a missing static file surfaces here rather than mid-deploy on Railway.

Also run Django's deployment lint:

```bash
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=... ALLOWED_HOSTS=princetonafeez.com ADMIN_ALLOWED_IPS=127.0.0.1 \
  python manage.py check --deploy
```

### GoDaddy DNS

1. In GoDaddy's DNS panel for `princetonafeez.com`:
   - **A record** at apex (`@`) → Railway's IPv4 if provided, otherwise use a forwarding domain.
   - **CNAME record** for `www` → Railway's provided hostname.
2. Lower TTL to 600 seconds before the cutover to speed up propagation if needed.
3. Verify with `dig princetonafeez.com` and `dig www.princetonafeez.com`.

### Cutover plan

The legacy 2020 JavaScript site is currently live at `princetonafeez.com`. To minimize the window where neither site is available:

1. Deploy the new site to Railway. Confirm it's reachable at the Railway-provided URL.
2. Smoke-test the new site at the Railway URL: every page renders, infinite scroll works, all docs links resolve to live GitHub anchors.
3. Update DNS at GoDaddy to point to Railway.
4. Wait for propagation (typically 10–60 minutes).
5. Verify HTTPS cert issuance on the custom domain (Railway handles this automatically).
6. Monitor Sentry and Railway logs for 24 hours.

---

## 21. Content Sync Strategy

### Source of truth

The file `content/apps.yaml` in this repository is the canonical source of app metadata and taxonomy metadata. It is version-controlled. Every change to the catalogue (new app, status update, stack revision, concept description) is a git commit. See ADR-0007.

### Manifest format

```yaml
stacks:
  python:
    name: Python
    category: language
  click:
    name: Click
    category: library
  pandas:
    name: pandas
    category: library

concepts:
  string-manipulation:
    name: String Manipulation
    description: "Cleaning, normalizing, and transforming user-provided text."
  cli-design:
    name: CLI Design
    description: "Command-line interface structure, flags, help text, and exit behavior."
  data-cleaning:
    name: Data Cleaning
    description: "Preparing messy input data for safer downstream use."
  csv-parsing:
    name: CSV Parsing
    description: "Reading, validating, and transforming comma-separated data."

apps:
  - name: String Sanitizer
    slug: string-sanitizer
    short_description: "Cleans and normalizes user input strings"
    status: completed
    build_order: 1
    github_url: https://github.com/PrincetonAfeez/String-Sanitizer
    completed_date: 2024-08-15
    stack: [python, click]
    concepts: [string-manipulation, cli-design]

  - name: CSV Cleaner
    slug: csv-cleaner
    short_description: "Removes duplicates, normalizes columns, fixes encoding"
    status: completed
    build_order: 2
    github_url: https://github.com/PrincetonAfeez/Csv-Cleaner
    completed_date: 2024-08-22
    stack: [python, click, pandas]
    concepts: [data-cleaning, csv-parsing, cli-design]

  # ... 88 more entries
```

### Seed command

`python manage.py seed_apps` reads `content/apps.yaml` and upserts the database. The manifest contains top-level `stacks`, `concepts`, and `apps` sections so taxonomy metadata is version-controlled instead of inferred:

- Stack and Concept rows are created or updated from their top-level manifest sections.
- App rows are upserted by `slug`. Existing apps have their fields updated; new apps are created.
- App `stack` and `concepts` values reference taxonomy slugs already defined in the same file.
- The command is idempotent — running it twice yields the same state.
- The command runs automatically after every deploy as part of the build command (after Tailwind compilation via npm, Python install, `collectstatic`, and `migrate`).

### Why a manifest and not the Django admin

The admin works but it's not the right source of truth. A YAML file in the repo:

- Is version-controlled with full diff history.
- Can be edited offline.
- Survives database wipes — re-run the seed command and the catalogue is restored.
- Lets the same data drive both prod and dev environments without copying database dumps.
- Documents the catalogue in a way humans can read and review in a pull request.

The Django admin remains as an escape hatch for emergency edits, but the manifest is primary.

---

## 22. Architecture Decision Records

Seven ADRs ship with v1 as a single compendium, [`docs/ADRS.md`](ADRS.md). Each ADR is a top-level section (`## ADR 0001 — …` through `## ADR 0007 — …`) following the standard format: **Status**, **Context**, **Decision**, **Consequences**, **Alternatives Considered**. The file notes that entries may be split into individual files under `docs/adr/` later if maintenance prefers that layout; the v1 repo ships one markdown file for simpler navigation and diff review.

| # | Title | Captures |
|---|---|---|
| 0001 | Django + HTMX monolith | Why Django, why HTMX, why not React/Next.js, why not a static site generator; also captures compiled Tailwind and self-hosted HTMX/Lucide |
| 0002 | PostgreSQL on Railway | Why Postgres in prod (not SQLite), why Railway over Fly/DO/Heroku, how the GoDaddy domain integrates |
| 0003 | Five docs via GitHub deep links | Why not store doc content in the database, why H2 anchors over H1, why one file per app over five files, the `docs_url` override field |
| 0004 | M2M for Stack and Concept | Why relational over free-text, even without v1 filtering |
| 0005 | HTMX infinite scroll with pagination fallback | The progressive-enhancement pattern, the dual-purpose view, accessibility considerations |
| 0006 | Logging strategy | JSON in prod, human-readable in dev, no file handler on Railway |
| 0007 | Content sync via manifest | Why a YAML manifest is source of truth, not the Django admin; top-level `stacks` and `concepts` taxonomy |

These ADRs are themselves a portfolio artifact. They demonstrate trade-off analysis applied to this project, mirroring the discipline of the five docs per catalogued app.

---

## 23. Out of Scope for v1

The following are explicitly out of scope for v1. Most appear in the roadmap below.

- Filtering or search on the apps catalogue
- Docker / containerization
- A blog or long-form writing section beyond ADRs
- Analytics
- RSS feed
- Dark mode toggle
- Multi-language support
- Comments or guestbook
- Newsletter signup
- Contact form
- User accounts of any kind
- Public API
- Markdown rendering on the site (docs remain on GitHub)
- Hospitality/Builder toggle on the home page (operator-first, single track)

---

## 24. Roadmap

### v1.1 — Catalogue navigation

- Add filter chips on `/apps/` (filter by stack, by status). Update the `app_list` view to honor query parameters. Update the HTMX infinite-scroll URL construction to preserve filters across loads.
- Add a search box on `/apps/` (server-side `icontains` query, no full-text indexing needed at this scale).

### v1.5 — Operational maturity

- Dockerize. `Dockerfile` and `docker-compose.yml` for local dev. Railway can still build from source, but Docker becomes an option.
- Add a writing section at `/writing/` for ADR-style technical notes beyond the apps catalogue.
- Add web analytics (privacy-respecting: Plausible or Fathom).

### v2 — Extension

- Render the documentation Markdown on the site directly, with a sync command pulling from GitHub. Decision deferred until v2 because of the trade-off of maintaining duplicate rendering pipelines.
- RSS feed for new apps.
- Dark mode.

---

## 25. Open Items and Assumptions

The following were assumptions during specification. Items marked **Confirmed** or **Resolved** are closed for v1; remaining items should still be validated when circumstances change.

1. **Confirmed (v1).** All 40 existing docs files follow the convention `{name_in_snake_case}_docs.md` at the repository root, with five H2 section headings (`## ADR`, `## TDD`, `## IDS`, `## Runbook`, `## Lessons Learned`).
2. **Confirmed (v1).** The default branch on every app repository is `main`, not `master`.
3. **Confirmed (v1).** Princeton's GitHub username is `PrincetonAfeez`. The seed manifest (`content/apps.yaml`) and app catalogue URLs use this organization consistently.
4. **Confirmed (v1).** The site contact email is `princetonafeez@gmail.com`, distinct from the resume's `Papresents@gmail.com`.
5. **Resolved (v1).** The headshot is committed in-repo at `static/img/headshot.png` and is not loaded from the legacy site at runtime.
6. **Open.** The current professional role is Interim General Manager at Crawford's Social, per the attached resume dated 2026. If a different current role is appropriate at launch time, the home page hero copy should be updated before deployment.
7. **Open until cutover.** The site is launched at `princetonafeez.com`, replacing the existing 2020 JavaScript site. DNS at GoDaddy will be updated to point at Railway as the final step of the cutover plan.

---

## Document control

This specification is the source of truth for v1. Any change to scope, architecture, or content plan should be reflected here via pull request. ADRs document the *why* behind individual decisions; this spec documents the *what* of the whole.
