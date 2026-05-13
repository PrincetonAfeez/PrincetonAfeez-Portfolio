# Architecture Decision Record
## App — Personal Portfolio Website
**Portfolio Platform Group | Document 1 of 5**
**Status: Accepted**

---

## Context

The Portfolio Platform group requires a production portfolio website that represents two audiences at once: hospitality decision-makers evaluating Princeton Afeez's operator background, and technical readers evaluating his Python and system architecture work. The site must communicate career history, provide contact and résumé access, and catalogue Python applications with links to source code and five documentation sections per app.

The repository is intentionally more than a résumé page. It is a deployed Django application with a database-backed catalogue, HTMX progressive enhancement, Tailwind CSS compilation, version-controlled app metadata, production security settings, CI, logging, Sentry support, and a Railway deployment path.

The decision was to build the portfolio as a Django + HTMX monolith with two Django apps: `pages` for the static marketing surface and `portfolio` for the dynamic apps catalogue.

---

## Decisions

### Decision 1 — Django + HTMX monolith over a JavaScript SPA

**Chosen:** Django 5, server-rendered templates, and HTMX for the catalogue's incremental loading behavior.

**Rejected:** React/Next.js, a separate frontend app, FastAPI plus a frontend framework, or a purely static site generator.

**Reason:** The portfolio's technical story is Python and system architecture. Django gives meaningful evidence of backend web competence: settings, URL routing, views, templates, ORM models, management commands, middleware, sitemaps, static files, deployment settings, testing, and security hardening. HTMX provides enough interactivity for infinite scroll without introducing a second application layer.

---

### Decision 2 — Separate `pages` and `portfolio` apps

**Chosen:** Use `pages` for static marketing pages and `portfolio` for the app catalogue.

**Rejected:** Putting all views, templates, content, models, and tests into one app.

**Reason:** The marketing surface and the app catalogue have different responsibilities. `pages` renders Princeton's professional story, contact page, résumé route, robots.txt, and error pages. `portfolio` owns the database-backed software catalogue, detail pages, taxonomy relationships, and documentation links. The split keeps the project readable and leaves the catalogue room to grow.

---

### Decision 3 — Relational catalogue with `App`, `Stack`, and `Concept`

**Chosen:** Model apps as database rows and represent technology/concept taxonomy with many-to-many relationships.

**Rejected:** Comma-separated tags, a JSON field, or rendering directly from YAML without a database.

**Reason:** The catalogue is expected to grow and eventually support filtering or search. `Stack` and `Concept` as first-class models make the data queryable and reusable. `App` can render detail pages, generate documentation URLs, expose absolute URLs, and participate in sitemaps. The cost is migrations, seed logic, and the need to prefetch relationships.

---

### Decision 4 — YAML manifest as source of truth

**Chosen:** Store catalogue metadata in `content/apps.yaml` and sync it into the database with `python manage.py seed_apps`.

**Rejected:** Treating the production database or Django admin as the canonical content source.

**Reason:** The catalogue is part of the portfolio artifact and should be version-controlled. A clean database can be rebuilt by running migrations and the seed command. This makes the portfolio reproducible from the repository rather than dependent on opaque database state. The admin remains available, but it is not the main content workflow.

---

### Decision 5 — GitHub deep links for the five app docs

**Chosen:** App detail pages render five buttons linking to ADR, TDD, IDS, Runbook, and Lessons Learned anchors in the app's GitHub documentation file.

**Rejected:** Copying or rendering all app documentation inside this portfolio site.

**Reason:** Each app's documentation belongs beside its source code. The portfolio acts as a discovery layer rather than a duplicated documentation host. This keeps the site smaller and avoids content drift. The trade-off is that documentation reading moves visitors to GitHub.

---

### Decision 6 — HTMX infinite scroll with progressive fallback

**Chosen:** `/apps/` uses Django pagination plus an HTMX `revealed` trigger to load the next page of app cards. A `<noscript>` link provides a fallback.

**Rejected:** One long page, traditional pagination only, or custom JavaScript IntersectionObserver logic.

**Reason:** The catalogue is long enough that loading everything upfront is unnecessary. HTMX lets the same server-rendered card partial support dynamic loading and normal pagination. The view detects `HX-Request` and returns either the full page or a partial. The app-list container uses `aria-live="polite"` for accessibility.

---

### Decision 7 — Compiled Tailwind CSS and vendored frontend scripts

**Chosen:** Tailwind is compiled from `static/css/tw-input.css` to `static/css/tw-compiled.css`, and HTMX/Lucide are vendored under `static/vendor/`.

**Rejected:** Tailwind Play CDN, Lucide/HTMX via external CDN, or a full frontend bundler.

**Reason:** Vendored scripts and compiled CSS support a strict production CSP with scripts and styles limited to `'self'`. The site avoids runtime CDN dependence for core interactivity and icons. The accepted trade-off is a Node/Tailwind build step in development, CI, and Railway deployment.

---

### Decision 8 — Environment-specific settings

**Chosen:** Separate `core.settings.base`, `dev`, `prod`, and `test` modules.

**Rejected:** One settings file with many conditionals.

**Reason:** Local development, production, and test execution need different behavior. Development enables Debug Toolbar and permissive hosts. Production enables PostgreSQL via `DATABASE_URL`, WhiteNoise manifest storage, CSP middleware, secure cookies, HTTPS redirect, Sentry, JSON logs, and fail-fast admin IP allowlisting. Test settings use a faster password hasher and pytest-specific configuration.

---

### Decision 9 — Admin protection through randomized path and IP allowlist

**Chosen:** Use `ADMIN_URL_PREFIX` for a randomized admin path and `AdminIPAllowlistMiddleware` to return 404 for admin requests outside `ADMIN_ALLOWED_IPS`. Production refuses to boot if `ADMIN_ALLOWED_IPS` is empty.

**Rejected:** Default `/admin/`, obscurity alone, or permissive admin access.

**Reason:** The site is public. A randomized admin prefix reduces obvious attack surface, but the IP allowlist is the real access control layer. Failing fast in production prevents accidental deployment with admin exposed behind only a hidden URL.

---

### Decision 10 — Railway deployment with PostgreSQL, Gunicorn, and WhiteNoise

**Chosen:** Deploy on Railway using PostgreSQL, Gunicorn, WhiteNoise, collectstatic, migrations, and seed command during build/deploy.

**Rejected:** GoDaddy shared hosting, a manually managed VPS, or SQLite production.

**Reason:** Railway supports GitHub-connected deployment, managed Postgres, environment variables, HTTPS, and stdout log aggregation with less operational burden. PostgreSQL is a credible production database. WhiteNoise lets Django serve static assets without another service.

---

## Consequences

**Positive:**
- The site honestly demonstrates Django/Python depth.
- Marketing pages and catalogue responsibilities are separated.
- Catalogue content is version-controlled and reproducible.
- App docs stay next to app source code.
- HTMX adds useful interaction without a frontend framework.
- Vendored scripts and compiled CSS support strict CSP.
- Production includes real security, logging, static-file, database, and deployment decisions.
- CI enforces CSS build, linting, formatting, template checks, migrations, seed command, tests, and coverage.

**Negative / Trade-offs:**
- Heavier than a static portfolio site.
- YAML and database can drift if admin edits are not backported.
- HTMX requires full/partial response branching.
- Tailwind requires Node when CSS must be rebuilt.
- Documentation links depend on GitHub file names and anchors.
- Railway deployment configuration is platform-specific.
- Development uses SQLite while production uses PostgreSQL.

---

## Alternatives Not Explored

- **Full CMS:** Rejected because the author maintains catalogue data as code.
- **On-site Markdown rendering:** Deferred to a possible v2 because it requires syncing, parsing, sanitization, caching, and link checking.
- **Client-side search/filtering:** Deferred; server-side filters fit Django/HTMX better.
- **Docker-first deployment:** Deferred because Railway/Nixpacks is adequate for v1.
- **Django admin as primary catalogue workflow:** Rejected because it makes content less reviewable and less reproducible.

---

*Constitution reference: Article 1 (architectural thinking), Article 3.4 (larger project classification), Article 4 (engineering quality), Article 6 (behavior verification), and Article 7 (progressive complexity).*

---


# Technical Design Document
## App — Personal Portfolio Website
**Portfolio Platform Group | Document 2 of 5**

---

## Overview

Personal Portfolio Website is a production Django + HTMX monolith for Princeton Afeez's professional portfolio and Python application catalogue. It serves static marketing pages, a database-backed apps catalogue, app detail pages, GitHub documentation links, résumé PDF delivery, robots.txt, sitemap.xml, custom error pages, protected admin access, and a Railway deployment pipeline.

**Project package:** `core`  
**Django apps:** `pages`, `portfolio`  
**Primary runtime:** Python 3.12  
**Framework:** Django 5.2  
**Production database:** PostgreSQL  
**Development database:** SQLite  
**Interactivity:** HTMX, vendored locally  
**Icons:** Lucide, vendored locally  
**Styling:** compiled Tailwind CSS  
**Deployment:** Railway + Gunicorn + WhiteNoise  
**Catalogue source:** `content/apps.yaml`

---

## Data Flow

### Full catalogue request

```
GET /apps/
     │
     ▼
portfolio.views.app_list()
     │
     ▼
App.objects.prefetch_related("stack", "concepts").order_by("-build_order")
     │
     ▼
Paginator(page_size=10)
     │
     ▼
No HX-Request header
     │
     ▼
render("portfolio/app_list.html", context)
     │
     ▼
HTML full-page response
```

---

### HTMX catalogue request

```
HTMX revealed trigger
     │
     ▼
GET /apps/?page=N with HX-Request header
     │
     ▼
portfolio.views.app_list()
     │
     ▼
same queryset + paginator
     │
     ▼
render("portfolio/partials/app_list_page.html", context)
     │
     ▼
partial HTML response
```

---

### App detail request

```
GET /apps/<slug>/
     │
     ▼
portfolio.views.app_detail(slug)
     │
     ▼
get_object_or_404(App.objects.prefetch_related(...), slug=slug)
     │
     ▼
render("portfolio/app_detail.html", {"app": app})
     │
     ▼
template calls {% doc_url app 'ADR' %}, etc.
     │
     ▼
HTML app detail page
```

---

### Catalogue seed flow

```
content/apps.yaml
     │
     ▼
python manage.py seed_apps
     │
     ▼
yaml.safe_load()
     │
     ├── stacks
     ├── concepts
     └── apps
     │
     ▼
Stack.objects.update_or_create()
Concept.objects.update_or_create()
App.objects.update_or_create()
     │
     ▼
app.stack.set(...)
app.concepts.set(...)
     │
     ▼
database reflects manifest
```

---

## Module-Level Structure

```text
PrincetonAfeez-Portfolio/
  manage.py
  core/
    settings/base.py
    settings/dev.py
    settings/prod.py
    settings/test.py
    context_processors.py
    logging_config.py
    middleware.py
    sitemaps.py
    urls.py
    wsgi.py
    asgi.py
  pages/
    content.py
    views.py
    urls.py
    templatetags/nav_tags.py
    templates/
    tests/
  portfolio/
    models.py
    views.py
    urls.py
    templatetags/doc_tags.py
    management/commands/seed_apps.py
    templates/portfolio/
    tests/
  content/apps.yaml
  static/css/
  static/vendor/
  static/js/
  static/resume/
  docs/
  requirements/
  package.json
  tailwind.config.cjs
  pyproject.toml
  railway.toml
  VERSION
```

---

## Module Dependency Graph

```
core.urls
  ├── pages.urls
  ├── portfolio.urls
  ├── pages.views.resume_pdf / robots_txt
  ├── django.contrib.admin
  └── django.contrib.sitemaps.views.sitemap

pages.views
  ├── pages.content constants
  ├── django.shortcuts.render
  ├── django.http.FileResponse / Http404 / HttpResponse
  └── django.urls.reverse

portfolio.views
  ├── portfolio.models.App
  ├── django.core.paginator.Paginator
  └── django.shortcuts.get_object_or_404 / render

portfolio.models
  ├── Stack
  ├── Concept
  ├── App
  ├── django.urls.reverse
  └── django.utils.text.slugify

seed_apps
  ├── yaml.safe_load
  ├── settings.BASE_DIR
  ├── Stack / Concept / App
  └── CommandError

core.settings.prod
  ├── dj_database_url
  ├── sentry_sdk
  ├── django-csp
  ├── WhiteNoise manifest storage
  └── ImproperlyConfigured admin allowlist check
```

---

## Core Data Structures

### `Stack`

Represents a technology used in an app.

```python
name: CharField(unique=True)
slug: SlugField(unique=True)
category: CharField(choices=CATEGORY_CHOICES)
```

Categories:
- language
- framework
- library
- tool
- database
- service

Ordering:
```python
["category", "name"]
```

---

### `Concept`

Represents a concept or skill demonstrated by an app.

```python
name: CharField(unique=True)
slug: SlugField(unique=True)
description: TextField(blank=True)
```

Ordering:
```python
["name"]
```

---

### `App`

Represents one portfolio application.

```python
name: CharField
slug: SlugField(unique=True)
short_description: CharField
status: CharField(choices=completed/in_progress/planned)
build_order: PositiveIntegerField(unique=True, db_index=True)
github_url: URLField
docs_url: URLField(blank=True)
hero_image: ImageField(optional)
completed_date: DateField(optional)
created_at: DateTimeField(auto_now_add=True)
updated_at: DateTimeField(auto_now=True)
stack: ManyToManyField(Stack)
concepts: ManyToManyField(Concept)
```

Ordering:
```python
["-build_order"]
```

---

### `DOC_ANCHORS`

```python
{
    "ADR": "adr",
    "TDD": "tdd",
    "IDS": "ids",
    "RUNBOOK": "runbook",
    "LESSONS_LEARNED": "lessons-learned",
}
```

Used by `App.doc_url()` to build GitHub documentation anchors.

---

### Site context

`core.context_processors.site_context()` injects:

```python
SITE_NAME
SITE_DOMAIN
SITE_VERSION
CONTACT_EMAIL
LINKEDIN_URL
GITHUB_URL
RESUME_URL
NAV_ITEMS
```

This avoids duplicating global site metadata in every view.

---

## Function and Class Reference

### `load_dotenv()`

A small custom dotenv loader in `core.settings.base`. It reads `.env`, skips blank/comment/invalid lines, and applies values with `os.environ.setdefault()`.

---

### `env_bool()` and `env_csv()`

Helpers for environment parsing. `env_csv()` powers settings such as `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `ADMIN_ALLOWED_IPS`.

---

### `AdminIPAllowlistMiddleware`

Protects the admin path. It builds the admin prefix from `settings.ADMIN_URL_PREFIX`, reads the client IP from `X-Forwarded-For` or `REMOTE_ADDR`, and raises `Http404` if the request targets admin from a disallowed IP.

---

### `build_logging_config(is_prod)`

Returns a Django `LOGGING` dictionary. Development uses human-readable console logs; production uses JSON console logs through `python-json-logger`.

---

### `StaticViewSitemap`

Includes:
- home
- about
- contact
- app list

---

### `AppSitemap`

Includes all `App` objects and uses each app's `updated_at` value as `lastmod`.

---

### `pages.views.home()`

Renders the home page with work history, capabilities, operator stack, certifications, and education from `pages.content`.

---

### `pages.views.about()`

Renders the about page with work history, capabilities, and operator stack.

---

### `pages.views.contact()`

Renders the contact page.

---

### `pages.views.resume_pdf()`

Serves `static/resume/resume.pdf` inline. Raises 404 if the file is missing.

---

### `pages.views.robots_txt()`

Returns robots.txt with:
- `Allow: /`
- `Disallow: /<admin-prefix>/`
- absolute sitemap URL

---

### `active_link` template tag

Returns `active` when the current request path matches the target route. Home must match exactly; non-home routes match by prefix.

---

### `App.docs_filename`

Generates the expected docs filename from the app name:

```python
slugify(name).replace("-", "_") + "_docs.md"
```

Example:
```text
String Sanitizer → string_sanitizer_docs.md
```

---

### `App.doc_url(doc_type)`

Builds a documentation URL. Uses explicit `docs_url` when present, otherwise falls back to `<github_url>/blob/main/<docs_filename>`, then appends the anchor.

---

### `portfolio.views.app_list()`

Fetches apps, prefetches stack/concepts, paginates at 10 per page, and returns either the full page or HTMX partial depending on the `HX-Request` header.

---

### `portfolio.views.app_detail()`

Fetches one app by slug and renders the detail page. Missing slugs return 404.

---

### `doc_url` template tag

Thin template wrapper around `app.doc_url(doc_type)`.

---

### `seed_apps` management command

Reads `content/apps.yaml`, creates/updates stacks and concepts, validates app taxonomy references, creates/updates apps, and sets many-to-many relationships. It is designed to be idempotent.

---

## Template Breakdown

### `portfolio/app_list.html`

Full catalogue page. Shows title, description, app count, GitHub link, and an `#app-list` region with `aria-live="polite"`.

---

### `portfolio/partials/app_list_page.html`

Renders app cards and, when another page exists, an HTMX trigger:

```html
hx-get="{% url 'portfolio:app_list' %}?page={{ next_page }}"
hx-trigger="revealed"
hx-swap="outerHTML"
```

Includes a `<noscript>` fallback link.

---

### `portfolio/app_detail.html`

Renders app name, build order, status, description, GitHub link, five documentation buttons, stack chips, concept chips, and structured data.

---

## State Management

### Database state

- SQLite locally by default
- PostgreSQL in production when `DATABASE_URL` is set
- Django auth/admin/session tables
- `App`, `Stack`, `Concept`, and many-to-many join tables

### Version-controlled content state

- `content/apps.yaml` is the canonical catalogue manifest
- `VERSION` provides the visible site version

### Static state

- compiled Tailwind CSS
- vendored HTMX and Lucide
- résumé PDF
- images and other static assets

### Environment state

- `.env` for local development
- Railway variables for production
- `ADMIN_ALLOWED_IPS` and `ADMIN_URL_PREFIX` for admin protection

---

## Error Handling Strategy

- Missing app slugs return 404 through `get_object_or_404`.
- Missing résumé PDF raises 404.
- Disallowed admin IPs raise 404.
- Production settings raise `ImproperlyConfigured` when `ADMIN_ALLOWED_IPS` is empty.
- `seed_apps` raises `CommandError` for missing manifest or missing taxonomy references.
- Custom 404 and 500 templates are configured.
- Sentry initializes when `SENTRY_DSN` is present.
- Production logs are structured JSON.

---

## External Dependencies

### Runtime / production

| Dependency | Purpose |
|---|---|
| Django | Web framework |
| Pillow | ImageField/image support |
| PyYAML | YAML manifest parsing |
| dj-database-url | DATABASE_URL parsing |
| WhiteNoise | Static files in production |
| python-json-logger | JSON production logs |
| django-csp | Content Security Policy |
| sentry-sdk | Error monitoring |
| gunicorn | WSGI server |
| psycopg | PostgreSQL driver |

### Development / testing

| Dependency | Purpose |
|---|---|
| django-debug-toolbar | Local debugging |
| pytest / pytest-django | Test runner and Django integration |
| playwright | Browser testing support |
| pytest-cov | Coverage |
| ruff | Linting |
| black | Formatting |
| djlint | Template linting |

### Node

| Dependency | Purpose |
|---|---|
| tailwindcss | CSS build |
| axe-core | Accessibility tooling support |

---

## Concurrency Model

The app is synchronous Django served by Gunicorn:

```bash
gunicorn core.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

There are no async views, task queues, background workers, custom threads, or websockets.

---

## Known Limitations

- No search/filter UI in v1.
- Docs are linked on GitHub rather than rendered on-site.
- Admin/database edits can drift from `content/apps.yaml`.
- SQLite dev database differs from PostgreSQL production.
- Railway deployment configuration is platform-specific.
- Contact is external-link/mailto only.
- Tailwind changes require a rebuild.
- No dedicated health-check endpoint.
- Résumé route depends on the PDF existing at the expected static path.

---

## Design Patterns Used

- Django MVT
- Django app separation
- Manifest-to-database sync
- Progressive enhancement with HTMX
- Template inheritance and partials
- Context processor for global metadata
- Template tags for view-adjacent logic
- Settings split by environment
- Fail-fast production configuration
- Structured logging factory
- Sitemap classes for static and dynamic URLs

---

## Verification Summary

The tests verify model methods, docs filename generation, docs URL generation, app absolute URLs, full and HTMX catalogue rendering, pagination, app detail success and 404 paths, seed command creation/idempotence, marketing pages, contact links, robots.txt, résumé PDF behavior, custom 404/500 pages, and CI coverage enforcement.

---

*Constitution reference: Article 4 (engineering quality), Article 6 (behavior verification), Article 7 (progressive complexity), and Article 8 (valid learner work).*

---


# Interface Design Specification
## App — Personal Portfolio Website
**Portfolio Platform Group | Document 3 of 5**

---

## Public Web Interface

| Method | Path | View / Handler | Success Status | Description |
|---|---|---|---:|---|
| `GET` | `/` | `pages.views.home` | 200 | Home page |
| `GET` | `/about/` | `pages.views.about` | 200 | About page |
| `GET` | `/contact/` | `pages.views.contact` | 200 | Contact page |
| `GET` | `/apps/` | `portfolio.views.app_list` | 200 | App catalogue |
| `GET` | `/apps/?page=N` | `portfolio.views.app_list` | 200 | Catalogue page N |
| `GET` | `/apps/<slug>/` | `portfolio.views.app_detail` | 200 | App detail |
| `GET` | `/resume.pdf` | `pages.views.resume_pdf` | 200 | Inline résumé PDF |
| `GET` | `/robots.txt` | `pages.views.robots_txt` | 200 | Robots file |
| `GET` | `/sitemap.xml` | Django sitemap view | 200 | Sitemap |
| `GET` | `/<ADMIN_URL_PREFIX>/` | Django admin | 200/302 if allowed | Protected admin |
| any | unknown route | custom 404 | 404 | Not found |

---

## Invocation Syntax

### Development server

```bash
python manage.py runserver
```

### CSS build

```bash
npm run build:css
```

### Database setup

```bash
python manage.py migrate
python manage.py seed_apps
```

### Tests

```bash
pytest
```

### Production process

```bash
gunicorn core.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

---

## Argument Reference Table

### `seed_apps`

```bash
python manage.py seed_apps [--path PATH]
```

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `--path` | path | No | `content/apps.yaml` | YAML manifest path |

---

### `npm run build:css`

| Script | Command | Description |
|---|---|---|
| `build:css` | `tailwindcss -i ./static/css/tw-input.css -o ./static/css/tw-compiled.css --minify` | Builds compiled Tailwind CSS |

---

## Input Contract

### `/apps/`

| Input | Type | Required | Description |
|---|---|---|---|
| `page` query parameter | int-like | No | Catalogue page number |
| `HX-Request` header | string | No | Returns partial template when present |

---

### `/apps/<slug>/`

| Input | Type | Required | Description |
|---|---|---|---|
| `slug` | slug string | Yes | App slug stored in DB |

Missing slug returns 404.

---

### `/resume.pdf`

Requires a file at:

```text
static/resume/resume.pdf
```

Missing file returns 404.

---

### `content/apps.yaml`

The seed command expects:
- top-level stack taxonomy
- top-level concept taxonomy
- app entries
- each app's stack/concept references to exist in taxonomy

---

## Output Contract

### `/apps/` full response

Successful full response includes:
- HTML document
- total app count
- app cards
- `id="app-list"`
- `aria-live="polite"`
- HTMX next-page trigger when more pages exist

---

### `/apps/` HTMX response

Successful partial response includes:
- app card HTML
- optional next-page HTMX trigger
- no full document wrapper

---

### `/apps/<slug>/`

Successful response includes:
- app name
- build order
- status
- short description
- GitHub link
- ADR/TDD/IDS/Runbook/Lessons Learned links
- stack chips
- concept chips
- structured data block

---

### `robots.txt`

```text
User-agent: *
Allow: /
Disallow: /<ADMIN_URL_PREFIX>/
Sitemap: <absolute sitemap URL>
```

---

### `resume.pdf`

Headers:

```text
Content-Type: application/pdf
Content-Disposition: inline; filename="resume.pdf"
```

---

## Exit Code Reference

The project uses standard Django/npm/pytest exit behavior.

| Command | Success | Failure |
|---|---:|---:|
| `python manage.py migrate` | 0 | non-zero on database/migration error |
| `python manage.py seed_apps` | 0 | non-zero on manifest/taxonomy/database error |
| `python manage.py collectstatic --noinput` | 0 | non-zero on static/config error |
| `npm run build:css` | 0 | non-zero on Node/Tailwind error |
| `pytest` | 0 | non-zero on test/setup error |
| `ruff check .` | 0 | non-zero on lint error |
| `black --check .` | 0 | non-zero on formatting error |
| `djlint ... --check` | 0 | non-zero on template lint error |

---

## Error Output Behavior

### Development

- Human-readable console logs.
- Debug mode enabled.
- Debug Toolbar enabled.

### Production

- Debug disabled.
- JSON logs to stdout.
- Sentry enabled when configured.
- Custom 404/500 pages.
- Disallowed admin IPs get 404.
- Missing `ADMIN_ALLOWED_IPS` prevents startup.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | Yes operationally | Settings module |
| `SECRET_KEY` | Yes in production | Django secret |
| `DEBUG` | No | Debug flag |
| `ALLOWED_HOSTS` | Yes in production | Comma-separated hosts |
| `CSRF_TRUSTED_ORIGINS` | Yes in production | Comma-separated trusted origins |
| `DATABASE_URL` | Yes in production | PostgreSQL URL |
| `ADMIN_ALLOWED_IPS` | Yes in production | Admin IP allowlist |
| `ADMIN_URL_PREFIX` | Recommended | Randomized admin route |
| `SENTRY_DSN` | Optional | Enables Sentry |
| `PORT` | Railway provided | Gunicorn bind port |

---

## Configuration Files

| File | Purpose |
|---|---|
| `.env` | Local environment values |
| `VERSION` | Site version string |
| `content/apps.yaml` | Canonical catalogue manifest |
| `requirements/base.txt` | Shared dependencies |
| `requirements/dev.txt` | Dev/test tooling |
| `requirements/prod.txt` | Production dependency include |
| `package.json` | Node scripts/dependencies |
| `tailwind.config.cjs` | Tailwind template scan config |
| `railway.toml` | Railway build/start commands |
| `pyproject.toml` | Black, Ruff, pytest, coverage, djlint config |

---

## Side Effects

| Operation | Side Effect |
|---|---|
| `npm run build:css` | Rewrites `static/css/tw-compiled.css` |
| `migrate` | Updates DB schema |
| `seed_apps` | Creates/updates catalogue rows and relationships |
| `collectstatic` | Writes collected assets to `STATIC_ROOT` |
| `createsuperuser` | Creates admin user |
| production boot with Sentry | Reports errors/traces to Sentry when configured |
| Railway deploy | Installs/builds/collects/migrates/seeds/starts app |

---

## Usage Examples

### Basic local use

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

### App catalogue

```text
http://127.0.0.1:8000/apps/
```

---

### App detail

```text
http://127.0.0.1:8000/apps/string-sanitizer/
```

---

### HTMX partial check

```bash
curl -H "HX-Request: true" "http://127.0.0.1:8000/apps/?page=2"
```

Expected: partial app-card HTML, not a full document.

---

### Seed from custom manifest

```bash
python manage.py seed_apps --path /path/to/apps.yaml
```

---

### Intentional failure — missing taxonomy

If an app references a stack or concept slug not declared in the manifest taxonomy, `seed_apps` raises an error identifying the missing reference.

---

## Public Python Interfaces

Important internal interfaces:
- `App.docs_filename`
- `App.doc_url(doc_type)`
- `App.get_absolute_url()`
- `portfolio.views.app_list`
- `portfolio.views.app_detail`
- `pages.views.resume_pdf`
- `pages.views.robots_txt`
- `core.context_processors.site_context`
- `AdminIPAllowlistMiddleware`
- `build_logging_config(is_prod)`
- `seed_apps` command

---

*Constitution reference: Article 4 (input/output boundaries), Article 6 (verification), and Article 8 (understandable and verifiable work).*

---


# Runbook
## App — Personal Portfolio Website
**Portfolio Platform Group | Document 4 of 5**

---

## Requirements

### Local development

- Python 3.12
- Node.js 20+
- npm
- Git
- pip/virtualenv
- SQLite default local database

### Production

- Railway project
- PostgreSQL service
- GitHub repository connected to Railway
- Required Railway environment variables
- Gunicorn
- WhiteNoise
- static asset build and collection

---

## Installation

```bash
git clone https://github.com/PrincetonAfeez/PrincetonAfeez-Portfolio.git
cd PrincetonAfeez-Portfolio

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/dev.txt

npm ci
npm run build:css

cp .env.example .env
python manage.py migrate
python manage.py seed_apps
python manage.py runserver
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Configuration Steps

### Development

Default local settings use:

```text
core.settings.dev
```

Behavior:
- debug enabled
- Debug Toolbar installed
- SQLite database
- human-readable logs
- permissive local hosts

---

### Test

Configured in `pyproject.toml`:

```text
DJANGO_SETTINGS_MODULE = core.settings.test
```

Behavior:
- fast password hasher
- test email backend
- pytest test discovery
- optional test database from `DATABASE_URL`

---

### Production

Set:

```text
DJANGO_SETTINGS_MODULE=core.settings.prod
SECRET_KEY=<strong-secret>
DEBUG=False
DATABASE_URL=<postgres-url>
ALLOWED_HOSTS=princetonafeez.com,www.princetonafeez.com
CSRF_TRUSTED_ORIGINS=https://princetonafeez.com,https://www.princetonafeez.com
ADMIN_ALLOWED_IPS=<comma-separated-ips>
ADMIN_URL_PREFIX=<randomized-prefix>
SENTRY_DSN=<optional>
```

---

## Standard Operating Procedures

### Run dev server

```bash
python manage.py runserver
```

---

### Rebuild CSS

```bash
npm run build:css
```

Run after changing Tailwind classes or source CSS.

---

### Fresh local database

```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_apps
```

---

### Add or update catalogue app

1. Edit `content/apps.yaml`.
2. Ensure taxonomy slugs exist.
3. Run:

```bash
python manage.py seed_apps
```

4. Verify `/apps/` and app detail page.
5. Commit YAML change.

---

### Run quality checks

```bash
ruff check .
black --check .
djlint pages/templates portfolio/templates --check
pytest --cov=core --cov=pages --cov=portfolio --cov-report=term-missing --cov-fail-under=70
```

---

### Production deploy

Railway build runs:

```bash
npm ci
npm run build:css
pip install -r requirements/prod.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_apps
```

Railway starts:

```bash
gunicorn core.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

---

## Health Checks

### Home page

```text
GET /
```

Healthy: HTTP 200 and professional positioning content.

---

### Catalogue

```text
GET /apps/
```

Healthy: HTTP 200, app cards, total count, `id="app-list"`.

---

### App detail

```text
GET /apps/string-sanitizer/
```

Healthy: HTTP 200, app title, five doc links, stack/concept chips.

---

### HTMX partial

```bash
curl -H "HX-Request: true" "/apps/?page=2"
```

Healthy: partial HTML and no full `<!doctype html>` wrapper.

---

### Robots and sitemap

```text
GET /robots.txt
GET /sitemap.xml
```

Healthy: robots disallows admin path and sitemap XML includes static/app URLs.

---

### Résumé PDF

```text
GET /resume.pdf
```

Healthy: HTTP 200, `application/pdf`, inline content disposition.

---

## Expected Output Samples

### `seed_apps`

```text
Seeded 14 stacks, 91 concepts, and 40 apps.
```

Counts vary with manifest changes.

---

### `robots.txt`

```text
User-agent: *
Allow: /
Disallow: /control-local/
Sitemap: http://127.0.0.1:8000/sitemap.xml
```

---

## Known Failure Modes

### Production refuses to start

**Trigger:** `ADMIN_ALLOWED_IPS` missing.

**Resolution:** Set `ADMIN_ALLOWED_IPS` in Railway and redeploy.

---

### Catalogue empty locally

**Trigger:** migrations or seed command not run.

**Resolution:**

```bash
python manage.py migrate
python manage.py seed_apps
```

---

### Styling stale

**Trigger:** Tailwind classes changed without rebuild.

**Resolution:**

```bash
npm run build:css
```

---

### Documentation buttons broken

**Trigger:** wrong `docs_url`, filename convention mismatch, or GitHub file moved.

**Resolution:** set explicit `docs_url` in `content/apps.yaml`, then rerun `seed_apps`.

---

### `seed_apps` missing taxonomy error

**Trigger:** app references undeclared stack/concept slug.

**Resolution:** add taxonomy entry or fix app reference.

---

### Résumé 404

**Trigger:** missing `static/resume/resume.pdf`.

**Resolution:** add the PDF at the expected path.

---

## Troubleshooting Decision Tree

```text
Site does not start
  ├── Missing SECRET_KEY?
  │     └── Set .env or environment variable
  ├── Production ADMIN_ALLOWED_IPS missing?
  │     └── Set allowlist
  ├── Database failure?
  │     └── Check DATABASE_URL and migrations
  └── Dependency failure?
        └── Install dev/prod requirements

Apps missing
  ├── Migrations not run?
  │     └── python manage.py migrate
  ├── Manifest not seeded?
  │     └── python manage.py seed_apps
  └── Seed error?
        └── Fix taxonomy references

Styling wrong
  ├── Tailwind not rebuilt?
  │     └── npm run build:css
  ├── Static files missing?
  │     └── collectstatic
  └── CSP/static error?
        └── Check browser console/network
```

---

## Dependency Failure Handling

### Python

```bash
python -m pip install -r requirements/dev.txt
```

Production:

```bash
python -m pip install -r requirements/prod.txt
```

---

### Node

```bash
npm ci
npm run build:css
```

---

### PostgreSQL

Check:
- `DATABASE_URL`
- Railway Postgres health
- migrations
- network binding

Then run:

```bash
python manage.py migrate
python manage.py seed_apps
```

---

## Recovery Procedures

### Broken local DB

```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_apps
```

---

### Bad manifest edit

1. Run `python manage.py seed_apps`.
2. Read missing taxonomy/error output.
3. Fix `content/apps.yaml`.
4. Rerun seed.
5. Commit fixed manifest.

---

### Bad production deploy

1. Check Railway logs.
2. Identify failing step.
3. Reproduce locally if possible.
4. Fix and push.

---

### Admin lockout

1. Confirm `ADMIN_URL_PREFIX`.
2. Confirm current public IP.
3. Add IP to `ADMIN_ALLOWED_IPS`.
4. Restart/redeploy.

---

## Logging Reference

### Development

Human-readable console logs:

```text
timestamp level logger message
```

### Production

JSON console logs with fields such as:
- timestamp
- level
- logger
- message
- module
- function name
- line number
- path name

Railway captures stdout.

---

## Maintenance Notes

- Keep `content/apps.yaml` canonical.
- Avoid making permanent catalogue edits only in admin.
- Rebuild CSS after template class changes.
- Run `seed_apps` after manifest changes.
- Keep docs filename/anchor conventions aligned with app repos.
- Keep `ADMIN_ALLOWED_IPS` current.
- Review CSP when adding scripts/assets/services.
- Add tests before adding search or filters.
- Consider Docker and a health endpoint in a future operational pass.

---

*Constitution reference: Article 6 (behavior verification), Article 5 (constraints and trade-offs), and Article 8 (verifiable learner work).*

---


# Lessons Learned
## App — Personal Portfolio Website
**Portfolio Platform Group | Document 5 of 5**

---

## Why This Design Was Chosen

This design was chosen because the portfolio needed to be both a professional website and a technical artifact. A static résumé page could tell Princeton's hospitality story, but it would not show Django architecture, database modeling, deployment decisions, testing, CI, static assets, security hardening, or documentation strategy.

Django + HTMX was the honest stack. It matches the author's Python/system architecture learning path and avoids pretending to be a JavaScript portfolio. The result is a site where the implementation reinforces the message: a disciplined operator learning software architecture through real, deployed systems.

The catalogue architecture was the most important decision. Version-controlled YAML gives reproducibility and reviewability; relational models give runtime queryability and room for filtering. That combination makes the app catalogue durable without giving up Django's ORM strengths.

---

## What Was Intentionally Omitted

**On-site rendering of app docs:** GitHub remains the documentation source of truth. This avoids sync/rendering complexity in v1.

**Search and filtering:** The data model supports it, but v1 keeps navigation reverse chronological.

**Contact form:** Contact uses email and LinkedIn. A form would require spam protection, validation, delivery, privacy copy, and monitoring.

**JavaScript framework:** HTMX provides the needed interaction without a separate frontend app.

**Docker:** Deferred because Railway/Nixpacks is sufficient for v1.

**CMS workflow:** YAML is easier to version, review, and reproduce for a single-developer portfolio.

---

## Biggest Weakness

The biggest weakness is the possibility of catalogue state drift. `content/apps.yaml` is intended to be canonical, but the database and Django admin still exist. If a permanent admin edit is not backported to YAML, a future seed or redeploy can overwrite it.

The second weakness is the external documentation reading experience. GitHub is appropriate for technical readers, but non-technical visitors may experience the docs links as a context switch.

The third weakness is dev/prod database asymmetry. SQLite is convenient locally, while PostgreSQL is production. CI mitigates this, but local development is not perfectly production-identical.

---

## Scaling Considerations

**If the catalogue grows:** add server-side search, stack/status/concept filters, indexes, and URL-preserved filter state.

**If documentation becomes central:** add a docs sync command, parse sections, store rendered content, cache results, and add broken-link checks.

**If traffic grows:** add a health endpoint, uptime monitoring, CDN review, database connection review, and Railway resource monitoring.

**If multiple maintainers contribute:** enforce manifest schema validation and document that YAML is canonical.

**If operational maturity increases:** add Docker, backup/restore docs, release checklist, and deployment smoke tests.

---

## What the Next Refactor Would Be

1. **Manifest schema validation** — catch missing fields, duplicate build orders, invalid statuses, unknown taxonomy, and malformed URLs before database writes.

2. **Catalogue filtering** — use the existing Stack/Concept many-to-many model for server-side filters with HTMX enhancement.

3. **Docs link checker** — verify that every generated documentation link resolves.

4. **Health endpoint** — expose a lightweight production readiness route.

5. **On-site docs rendering in v2** — keep GitHub canonical but provide a first-party reading experience.

---

## What This Project Taught

- **A portfolio can be a system, not just a page.** The site demonstrates the same architectural thinking it claims the author is learning.

- **Honest stack choice matters.** Django + HTMX reflects real Python depth better than a superficial JavaScript framework portfolio.

- **Content needs ownership.** YAML as source of truth makes the catalogue reviewable, diffable, and reproducible.

- **Progressive enhancement is practical.** HTMX infinite scroll improves browsing without breaking no-script fallback.

- **Security belongs in small projects too.** Admin allowlisting, strict CSP, secure cookies, HSTS, HTTPS redirect, JSON logs, and Sentry are appropriate for a public portfolio.

- **Tests should protect real user paths.** The tests cover pages, catalogue behavior, docs links, HTMX partials, seed command, résumé delivery, robots.txt, and error pages.

- **Deployment is part of architecture.** Railway, Gunicorn, PostgreSQL, WhiteNoise, collectstatic, migrations, seeding, CI, and logging are all design decisions.

---

*Constitution v2.0 checklist: This document satisfies Article 5 (trade-off documentation), Article 6 (verification), and Article 7 (progressive complexity) for the Personal Portfolio Website.*
