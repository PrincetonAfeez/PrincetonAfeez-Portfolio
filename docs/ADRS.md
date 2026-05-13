# Architecture Decision Records

**Project:** princetonafeez.com portfolio
**Author:** Princeton Afeez
**Status:** All decisions Accepted, May 2026
**Format:** Each ADR documents one decision in the format Status / Context / Decision / Consequences / Alternatives Considered.

This compendium captures the seven architectural decisions that shape the v1 build of the portfolio site. They are presented together for ease of reading; in the repository they may be split into individual files under `docs/adr/` if that proves easier to maintain.

---

## ADR 0001 — Django + HTMX monolith

### Status

Accepted, May 2026.

### Context

The portfolio site has two competing constraints. It must demonstrate technical maturity — server-side architecture, data modeling, testing, deployment, observability — at a level credible to a senior engineer reviewing the work. At the same time, the author has spent the last twelve months focused on Python and system architecture, not on JavaScript frameworks, and a portfolio that misrepresents the actual skill being built would fail an interview in the first technical question.

The site is small. A handful of static marketing pages, one dynamic catalogue with a hundred or so entries, and one detail page per entry. There is no real-time interactivity, no user accounts, no public API, no client-state that needs to live in the browser. The only meaningful interaction beyond navigation is incremental loading of catalogue entries.

The site is also a capstone. The architecture choices are themselves part of what the site is demonstrating. Choosing a stack purely for familiarity or speed would undercut the portfolio's purpose.

### Decision

The web layer is Django 5. Interactivity is provided by HTMX. Styling uses Tailwind utility classes from a **compiled** CSS bundle: a small Tailwind 3 pipeline (`tailwind.config.cjs`, `static/css/tw-input.css` → `static/css/tw-compiled.css`) runs via `npm run build:css` in local development, CI, and Railway before `collectstatic`. HTMX and Lucide are **self-hosted** first-party static files under `static/vendor/` (not third-party script CDNs). There is no JavaScript framework. There is no separate frontend application. The entire request lifecycle — routing, query, render — happens in Python returning HTML.

Templates use a three-level inheritance structure (`base → layout → page`) with a small library of component and section includes. Server-rendered partials handle the one dynamic interaction the site has (infinite scroll on the apps catalogue).

### Consequences

**Positive.** The stack accurately represents the author's current skill set. Every part of the site is Python; an interviewer reading the code sees consistent depth. The mental model is simple: one process, one language, one templating system. Server-side rendering gives strong SEO defaults and fast first paint. The only front-end build step is Tailwind CSS compilation — no Webpack, no Vite, no application JavaScript transpilation. Self-hosted HTMX and Lucide keep production CSP strict (`script-src` and `style-src` limited to `'self'`) without relying on `cdn.tailwindcss.com` or `unpkg.com`.

**Negative.** The site does not demonstrate experience with a JavaScript framework, which many employers list. The author accepts this; the portfolio is honest about what the author actually knows, and a misrepresented React portfolio is worse than no React portfolio. HTMX has a smaller community than React; documentation and Stack Overflow answers are thinner. If HTMX ever proves limiting for a future feature, a migration to a JS framework would be a meaningful rewrite of the catalogue interactions.

The Tailwind build adds Node.js as a prerequisite wherever CSS must be regenerated (local dev after template class changes, CI, and Railway). Mitigated by committing `tw-compiled.css` and running `npm ci && npm run build:css` in the deploy pipeline so production never drifts silently from templates.

The "no forms" constraint that follows from this choice (contact is `mailto:` only) removes a class of features the site might otherwise have offered.

### Alternatives considered

**Next.js + React.** The mainstream choice for a 2026 portfolio. Rejected because it doesn't match the author's actual study, and because the site is small enough that the SPA architecture imposes complexity without proportional benefit.

**Flask + Jinja2.** Lighter than Django, same Python-only model. Rejected because Django's batteries — ORM, admin, migrations, security middleware, sitemap framework, auth scaffolding — are the things being demonstrated. Choosing Flask would shrink the architectural surface the portfolio shows.

**FastAPI + a frontend framework.** Violates the "all Python web layer" constraint. Also imposes the dual-stack complexity the site doesn't need.

**A static site generator (Pelican, Hugo, Jekyll).** Workable for the marketing pages but cannot support a dynamic catalogue, infinite scroll, or future filtering without significant build-time machinery. Rejected because the catalogue is the point of the site, and giving up dynamic content to gain build simplicity is the wrong trade for this project.

**Plain Django with no HTMX.** Works but loses the progressive-enhancement demonstration that makes infinite scroll possible. Rejected because the infinite scroll is itself an architectural artifact worth showing, and ADR-0005 captures real trade-off analysis around it.

---

## ADR 0002 — PostgreSQL on Railway, GoDaddy as registrar only

### Status

Accepted, May 2026.

### Context

The site needs a production database and a host. The domain `princetonafeez.com` is already registered at GoDaddy, where the legacy 2020 JavaScript site is currently served. The initial assumption was that GoDaddy would also host the new Django application, on the basis that the registrar and the host should be the same vendor.

GoDaddy's shared hosting plans are built for PHP/WordPress and static sites. They do not natively support Django. Their VPS and dedicated server plans can technically run Django but require the operator to install and maintain Python, PostgreSQL, nginx, gunicorn, and SSL certificates manually. For a site that intends to demonstrate production maturity (CI/CD, JSON logging, security headers, observability), GoDaddy hosting would fight nearly every requirement.

The author is a solo developer optimizing for shipping a credible v1, not for the educational value of running a server. The operational learning is captured in ADR-0006 (logging) and elsewhere; managing a Linux VM is not part of the portfolio's purpose.

### Decision

GoDaddy remains the domain registrar. Hosting moves to Railway. Railway provisions the Django application from the GitHub repository and a managed PostgreSQL service. DNS at GoDaddy is updated to point the apex (`@`) and `www` records at Railway.

PostgreSQL 16 is the production database. The development environment uses SQLite for speed and simplicity; production uses Postgres for the standard reasons (concurrency, indexing, data types, parity with the kind of database Princeton would encounter in any real engineering role).

### Consequences

**Positive.** Deploys are GitHub-triggered, with auto-deploy from `main` after CI passes. HTTPS certificates are issued and renewed by Railway with no operator action. The PostgreSQL service is a one-click add and provides `DATABASE_URL` as an environment variable, eliminating an entire category of connection-string handling. Logs from stdout are captured and aggregated automatically; the logging strategy in ADR-0006 leans on this. Railway's pricing for a portfolio-scale site is approximately $5–20/month.

**Negative.** Lock-in to Railway's deployment model. A future migration to Fly.io, DigitalOcean App Platform, or self-hosted infrastructure would require rewriting the deploy configuration, redoing log capture, and re-establishing TLS and DNS. The risk is modest because the application itself is portable Django + Postgres, but the operational glue is platform-specific.

The dev/prod database asymmetry (SQLite local, Postgres prod) introduces a class of bugs that only appear in production. Mitigated by running CI against PostgreSQL and by avoiding SQLite-specific SQL features, but not eliminated.

### Alternatives considered

**GoDaddy hosting.** Examined and rejected for the reasons in Context. The cost of forcing Django onto GoDaddy infrastructure is operational complexity that defeats the "production-grade with reasonable effort" goal.

**Fly.io.** A serious candidate. Offers more control than Railway and a more sophisticated networking model. Rejected for v1 because the additional control comes with additional configuration; Railway ships the same site faster with less to learn at the platform layer. Fly.io remains a credible future migration target if Railway's pricing or feature set ever stops fitting.

**DigitalOcean App Platform.** Comparable to Railway in feature set, slightly more expensive at the relevant tier, mature and stable. Rejected because Railway's GitHub integration and the YAML-free configuration model are smoother for a solo developer.

**Heroku.** Historically the obvious choice for this kind of site. Rejected because pricing has moved unfavorably for hobby-tier projects since the free tier was discontinued, and because Railway and Fly.io now match Heroku's ergonomics at lower cost.

**A VPS (DigitalOcean droplet, Hetzner, Linode).** Maximum control, lowest cost, highest operational burden. Rejected because the operational work (server provisioning, hardening, certificate renewal, deployment scripting, log management) is not what the portfolio is trying to demonstrate. The author would rather show clean application architecture than a hand-rolled deployment pipeline.

**SQLite in production.** Briefly considered for cost reasons. Rejected because production-grade was a stated requirement, and "production-grade Django" implies a real database. SQLite works at this scale but signals the wrong thing to a technical reviewer.

---

## ADR 0003 — Five docs surfaced via GitHub deep links, not on-site rendering

### Status

Accepted, May 2026.

### Context

Each app in the catalogue ships with five documentation sections: Architecture Decision Record (ADR), Technical Design Document (TDD), Interface Design Specification (IDS), Runbook, and Lessons Learned. The author has been writing these consistently across the existing forty apps using a shared template, and intends to continue the practice for the next fifty.

The original convention stored the five sections as a single Markdown file per app at the repository root, named in lowercase snake_case with the suffix `_docs.md` (e.g., `string_sanitizer_docs.md` in the `String-Sanitizer` repository). Section headings within the file used H1 (`#`).

The portfolio site needs to make these documents discoverable. The question is whether to render them on the site, link to them externally, or some combination.

This is the single highest-leverage architectural decision in the project. The five-doc practice is the portfolio's strongest differentiator; how it is surfaced determines whether visitors actually see the depth of work.

### Decision

Documentation link strategy is orthogonal to how the site loads CSS and JavaScript; see ADR-0001 for compiled Tailwind and self-hosted HTMX/Lucide.

The documentation is not duplicated on the portfolio site. It remains in each app's GitHub repository as the single source of truth. The app detail page renders five buttons, one per doc section, each linking directly to the relevant H2 anchor on GitHub's rendered Markdown view.

Two corrections to the original convention are made as part of this decision:

1. **Section headings change from H1 to H2.** H1 is reserved for the document title (one per document). Multiple H1 headings break semantic structure, confuse screen readers, and interact poorly with GitHub's table-of-contents rendering. The five section headings become `## ADR`, `## TDD`, `## IDS`, `## Runbook`, `## Lessons Learned`. A single `# <App Name> Documentation` H1 sits at the top of each file. The existing forty files will be migrated with a scripted rename ahead of v1 launch.
2. **The site does not render or fetch the Markdown.** No GitHub API calls, no copying of files into the portfolio repository, no rendering pipeline. The buttons are plain anchor tags to URLs constructed from the app's manifest-backed `docs_url` and a known anchor. If `docs_url` is ever omitted for a future app, the model can fall back to the default filename convention.

### Consequences

**Positive.** Zero content duplication. The Markdown lives next to the code it describes, which is where it belongs and where it will be kept in sync. No build dependency on GitHub's API. No tokens to manage. No content-drift problem. The portfolio site stays small and fast. The five-button cluster on each detail page is visually legible as a differentiator even though all five links point into the same file.

**Negative.** Visitors leave the portfolio site to read documentation, which weakens the site's session metrics and means GitHub's rendering controls the styling of the documents (the site cannot theme them). If a documentation file is renamed, moved into a `/docs/` subdirectory, or a repository is made private or deleted, the manifest URL must be updated or the links break and the failure is silent. The H2 anchor convention depends on GitHub's anchor-generation algorithm staying stable; if GitHub ever changes how `#lessons-learned` is generated from `## Lessons Learned`, all anchor links break simultaneously.

The decision delegates a meaningful part of the user experience to GitHub. This is acceptable for a portfolio site whose audience includes technical readers who are familiar with GitHub, and is a reasonable trade for the architectural simplicity it provides.

### Alternatives considered

**Render the Markdown on-site via GitHub API at build time.** A management command fetches each app's `_docs.md` file via the GitHub API, parses the five sections, renders them with a Markdown library, and stores the HTML in the database. Detail pages render the cached HTML inline. Rejected because the complexity is significant (API auth, rate limits, sync command, parse logic, render-time HTML escaping for code blocks) and the benefit (visitor doesn't leave the site) is modest. Reconsidered for v2.

**Render the Markdown on-site by copying files into the portfolio repository.** A pre-commit script copies the latest `_docs.md` from each app repository into a `content/docs/` directory in the portfolio repository. Build-time rendering happens from the local copy. Rejected because it creates a duplicate source of truth that will inevitably drift, and because cross-repository pre-commit hooks are an operational headache.

**Iframe-embed the GitHub-rendered Markdown.** Lowest effort; visually inconsistent with the site, breaks responsive layout, controlled by GitHub's frame headers (which deny `frame-ancestors`, making this impossible without a proxy). Rejected.

**A single "View Documentation" button linking to the file root, no deep links.** Hides the five-doc differentiator. A visitor who clicks lands on the top of the document and may not realize the five distinct sections exist. Rejected because the five-doc structure is the differentiator and the buttons need to make it visible.

**One Markdown file per doc per app (five files per app, 450 files total).** The original alternative to the single-file convention. Rejected because it inflates the file count by 5x, increases maintenance friction (five files to update per app), and offers no real benefit over deep-linking within a single well-structured file.

---

## ADR 0004 — Many-to-many models for Stack and Concept, despite no v1 filtering

### Status

Accepted, May 2026.

### Context

Each app in the catalogue is associated with a set of technologies (e.g., Python, Click, pytest) and a set of concepts (e.g., string manipulation, CLI design, REST APIs). The catalogue's v1 navigation is purely reverse-chronological; there is no filtering, no search, no concept index. Filtering is on the v1.1 roadmap.

The minimal viable representation of these associations is a free-text field on the `App` model: a comma-separated string of tags. This is simple and fast. The relational representation is two separate models (`Stack` and `Concept`) with many-to-many relationships to `App`. This is more architecture and requires migrations.

The question is which to ship in v1.

### Decision

Use proper many-to-many relationships. `Stack` and `Concept` are first-class models with their own table, slug, name, and category (in Stack's case). `App` has `models.ManyToManyField` references to both, with Django's default through-tables.

No through-model fields are added in v1. If display ordering of chips ever matters, a custom through model can be introduced via a single schema migration without changing the public API of the relationship.

### Consequences

**Positive.** The data model is correct from the start. When v1.1 adds filtering, the change is a UI feature, not a data migration: the `App.stack` and `App.concepts` reverse managers already support `.filter(stack__slug='django')` and similar queries. The chip rendering on app detail pages can use the related `name` and `slug` for both display text and CSS classes without any text-splitting logic. Counts of apps per stack or concept become a one-line query, making future "apps using Django" type views trivial.

**Negative.** The catalogue list view requires `prefetch_related('stack', 'concepts')` to avoid N+1 queries — easy to forget and easy to verify with `django-debug-toolbar` locally. The seed command must handle two extra layers (creating `Stack` and `Concept` rows on first reference). The admin has three models to manage instead of one.

### Alternatives considered

**Free-text `CharField` on `App`.** Simplest implementation. Rejected because filtering is on the roadmap, and the data migration from free-text tags to a normalized relationship is the kind of work that gets deferred indefinitely. Doing it once now is cheaper than doing it later under feature pressure.

**`JSONField` containing a list of strings.** Queryable in PostgreSQL via `__contains`, no extra tables, less ceremony than M2M. Rejected because it loses the relational benefits (no concept of "a concept exists independently of any app using it"), and because PostgreSQL JSON indexing is more involved than a standard B-tree index on a slug column.

**`django-taggit`.** A well-maintained library providing generic tagging. Rejected because it solves a more general problem than this project needs, introduces a dependency for a feature that is already two-model-files of code, and conflates Stack and Concept into a single "tag" namespace where the project wants them separated.

**Two separate through-models from day one.** Adds `AppStack` and `AppConcept` explicit models with `order` and `created_at` fields. Rejected because v1 has no use for the extra fields, and the through-model can be added later via `db_table` preservation when the need arises.

---

## ADR 0005 — HTMX infinite scroll with progressive-enhancement pagination fallback

### Status

Accepted, May 2026.

### Context

The apps catalogue will eventually hold roughly ninety entries — the forty existing apps plus the fifty planned. The author has stated mobile-first as a design constraint and reverse chronological as the default sort order.

Three navigation patterns are viable: a single long page rendering all apps, traditional server-side pagination, and infinite scroll. Each has implications for performance, accessibility, SEO, and the demonstration value of the architecture itself.

The site is also intended to be a credible HTMX demonstration. The author has not previously shipped an HTMX feature, and the catalogue is the most natural place to introduce one.

### Decision

The catalogue uses HTMX-driven infinite scroll for the primary path and progressive enhancement to fall back to traditional pagination when JavaScript is disabled. A single Django view handles both paths.

On initial load, the catalogue renders the first ten apps. Below the last card, an HTMX sentinel with `hx-trigger="revealed"` fires when scrolled into view, fetching the next ten cards as a partial template. The server distinguishes partial requests from full-page requests via the `HX-Request` header. A **`<noscript>`** block with a real anchor to `?page=2` sits **outside** the `aria-hidden` HTMX wrapper so the no-JavaScript path stays available to assistive technologies; the same view renders the full page template for that navigation.

The HTMX-loaded content is announced to assistive technologies via an `aria-live="polite"` region wrapping the app list.

### Consequences

**Positive.** Mobile performance is good: initial page weight is small, subsequent loads are partial HTML payloads, no JavaScript bundle beyond HTMX's ~14KB. Search engine crawlers and screen reader users get a paginated experience that works without JavaScript. The single-view pattern keeps server code compact. The decision is itself an architectural artifact: progressive enhancement is a meaningful concept to demonstrate, and the `HX-Request` header pattern is real-world HTMX.

**Negative.** The view logic forks on a request header, which is a less common pattern than two separate views and can confuse a reviewer who hasn't seen it. Filter state in v1.1 will need to thread through both the HTMX URL and the `<noscript>` anchor, which doubles the surface area of "did I update both query-string handlers." If a future feature requires per-card interactivity (e.g., favoriting, in-place edits), the infinite scroll's append semantics need to coexist with whatever per-card swap pattern is introduced; this is solvable but worth flagging.

The `aria-live` region must be tuned carefully: setting it on the wrong container can cause screen readers to announce every card or, worse, announce them all at once on initial load. Testing with VoiceOver and NVDA is part of the v1 accessibility pass.

### Alternatives considered

**Traditional server-side pagination only.** Simplest, most accessible by default, no JavaScript at all. Rejected because the site is intended to demonstrate HTMX and infinite scroll is the more natural mobile experience for a long flat list.

**A single long page rendering all 90 apps.** Loads everything upfront, no pagination logic, ideal for SEO. Rejected because page weight grows linearly with the catalogue, mobile scroll position is fragile, and the user experience degrades as the catalogue grows.

**Client-side infinite scroll via Intersection Observer.** Pure JavaScript, no server-side request differentiation. Rejected because the site is committed to "all Python web layer" (ADR-0001), and writing a custom IntersectionObserver implementation steps outside that constraint.

**Two separate views (one for HTMX, one for full-page).** Cleaner separation of concerns. Rejected because the two views would share 95% of their logic, and keeping them in sync as filters and sort options are added in v1.1 would be a maintenance burden. The `HX-Request` header is the idiomatic HTMX pattern for exactly this case.

**"Load more" button instead of scroll-triggered.** Less magical, more explicit, easier to test. Rejected because mobile users expect scroll-triggered loading and the button adds an extra tap. The `revealed` trigger is the right default; a button could be added in v1.1 if user feedback suggests it.

---

## ADR 0006 — JSON logging in production, human-readable in development

### Status

Accepted, May 2026.

### Context

The site needs logging that supports two distinct activities. In development, the author tails logs in a terminal while iterating on code; the priority is human readability and high signal-to-noise. In production on Railway, logs are captured from stdout and aggregated by Railway's log viewer (with the option to forward to Datadog, Loki, or another aggregator later); the priority is structured data that can be filtered and queried.

A single log format cannot serve both well. Human-readable text is hard to parse mechanically; JSON is hard to read in a terminal without tooling.

### Decision

Logging is configured by a single function, `core.logging_config.build_logging_config(is_prod: bool)`, which returns a Django `LOGGING` dictionary. The function is called from `core/settings/base.py` using a boolean derived from the environment.

**Development:** one console handler. Human-readable formatter (`%(asctime)s %(levelname)-8s %(name)s %(message)s`). Application loggers at `DEBUG`, Django at `INFO`.

**Production:** one console handler (Railway captures stdout; no file handler is needed). JSON formatter via `python-json-logger`, emitting `timestamp`, `level`, `logger`, `message`, `module`, `funcName`, `lineno`, `pathname`. Application loggers at `INFO`, Django at `WARNING`.

### Consequences

**Positive.** Local development stays ergonomic — terminal output is glanceable, errors are easy to spot. Production logs feed cleanly into Railway's aggregation and any future structured-log destination. The two configurations live in one function in one file; the asymmetry is documented in code rather than spread across settings modules. There is no file handler in production, which removes a class of problems (disk fill, log rotation, file permissions) that Railway's stdout-capture model makes irrelevant.

**Negative.** The two formats mean a developer occasionally inspecting production logs locally (e.g., via `railway logs` piped to a file) will see JSON, which is harder to skim than the dev format. Mitigated by tools like `jq` or by Railway's web UI, which renders JSON logs as expandable rows. The asymmetry could surprise a future contributor; the ADR itself is the mitigation.

If hosting ever moves off Railway to a platform that doesn't capture stdout, the production logging config will need to add file handlers and a rotation policy. This is a small change but worth noting.

### Alternatives considered

**JSON everywhere.** Consistency across environments. Rejected because local terminal readability is too valuable to sacrifice, and the development workflow runs more iterations than the production triage workflow.

**Human-readable everywhere.** Same consistency argument. Rejected because production log aggregators want structure, and grep-based investigation across a JSON-less log stream is slow.

**File handlers in production in addition to stdout.** A defense-in-depth pattern. Rejected because Railway's filesystem is ephemeral (container restarts wipe state) and the stdout capture is the canonical log destination. Adding file handlers would create the illusion of durability without the substance.

**`structlog`.** A more powerful structured-logging library with first-class context propagation. Rejected for v1 because it imposes a different API on application code (`logger.info("event", key=value)` rather than the standard `logger.info("message")`), and the standard library plus `python-json-logger` covers the use case adequately. `structlog` is a credible v2 upgrade if context propagation becomes a need.

**Loguru.** Simpler API than the standard library. Rejected for the same reason as `structlog` plus the additional concern that it deviates from idiomatic Django logging, making the codebase harder to read for any future contributor familiar with the standard library.

---

## ADR 0007 — Content sync via version-controlled YAML manifest, not Django admin

### Status

Accepted, May 2026.

### Context

The catalogue will hold approximately ninety apps. Each app has metadata: name, slug, short description, status, build order, GitHub URL, completion date, associated stack technologies, and associated concepts. This metadata changes regularly — new apps are added, statuses change from "planned" to "in progress" to "completed," and existing apps occasionally gain new associated concepts as the author's understanding sharpens.

The question is where this metadata lives. Django's default model is the admin: superuser logs in, edits the data, changes persist in the database. This works but treats the database as the source of truth, which has implications for version control, backup, and reproducibility.

The catalogue itself is content the author cares about preserving across database changes, host migrations, and disaster scenarios. It is also a portfolio artifact in its own right — a reviewer reading the repository should be able to see the catalogue as code, not just as a rendered website.

### Decision

The file `content/apps.yaml` in this repository is the canonical source of truth for app metadata and taxonomy metadata. The file is version-controlled. Every change to the catalogue (new app, status update, stack revision, concept description) is a git commit.

A management command, `python manage.py seed_apps`, reads `apps.yaml` and upserts the database. The command is idempotent: running it on a clean database produces the same state as running it on a populated database. It creates or updates `Stack` and `Concept` rows from top-level taxonomy sections, then creates or updates `App` rows by slug and attaches each app to taxonomy entries by slug.

The command runs in Railway’s **`preDeployCommand`** (with `DATABASE_URL` available), chained after **`migrate`** and before new application containers start serving traffic — not during the image **build**, which only compiles assets and runs **`collectstatic`**. Every successful deploy reflects the current state of `apps.yaml`. The Django admin remains enabled and functional, but is treated as an escape hatch for emergency edits rather than the primary content workflow.

### Consequences

**Positive.** The catalogue is diff-able. Pull requests for catalogue changes are reviewable like code changes. The catalogue survives database wipes — a fresh deploy with an empty database becomes a fully-populated catalogue after the seed step. Local development and production use the same canonical content without dump-and-restore workflows. The repository tells the full story of the portfolio, not just the site that renders it. The catalogue can be regenerated in another database technology, another host, another framework, without losing data.

**Negative.** Two sources of truth exist if a future maintainer uses the admin and forgets to backport the change to `apps.yaml`. Mitigated by treating admin as escape-hatch only and by documenting the workflow in the README; not eliminated. The deploy pipeline runs **`seed_apps`** in **pre-deploy** (after migrations), which adds a short step before new containers start. The seed command must be maintained as a real piece of code (with tests) rather than a one-off script.

YAML editing is more friction than admin form editing for non-developers. This is acceptable because the catalogue is maintained by the author, who is a developer.

### Alternatives considered

**Django admin as the primary content workflow.** The default, lowest-friction option. Rejected because it surrenders version control of the catalogue, makes review and rollback awkward, and ties the canonical content to a specific database instance.

**Database fixtures (Django's `loaddata`/`dumpdata`).** Built-in mechanism for serialized model state. Rejected because JSON or XML fixtures are harder to read and edit than YAML, fixture files tend to grow brittle as schemas evolve, and the workflow forces a `dumpdata` step after admin edits to keep the fixture current — recreating the same dual-source-of-truth problem the manifest avoids.

**A JSON manifest instead of YAML.** Same architectural benefits, more verbose for nested data, no comment support. Rejected because YAML's readability advantage matters at the scale of ninety entries with nested arrays of stack and concept references.

**Markdown front-matter in each app's `_docs.md`, fetched at sync time.** Distributes the metadata next to the docs it describes. Considered seriously; rejected because it introduces a runtime dependency on the GitHub API (or a build-time fetch step), and the metadata wants to live with the portfolio site rather than with each app's individual repository.

**Database as source of truth, with an export command.** Inverse of the chosen approach: admin is canonical, a `python manage.py dump_apps` command writes out a YAML snapshot on demand. Rejected because the export becomes stale the moment it's written, and version control over a stale export is less valuable than version control over the live source.

---

## Cross-cutting notes

These seven decisions interact in ways worth naming explicitly.

The combination of ADR-0001 (Django + HTMX), ADR-0005 (infinite scroll with progressive enhancement), and ADR-0007 (manifest-driven content) means the entire site can be reconstructed from the repository plus the linked GitHub repositories. The portfolio is fully reproducible: clone the repo, run the seed command, deploy. Nothing of value lives in a database that isn't also in version control.

The combination of ADR-0003 (docs on GitHub) and ADR-0007 (content as manifest) means the portfolio site is small. It catalogues but does not contain. This is a deliberate choice: the site's job is to surface and link, not to host.

The combination of ADR-0002 (Railway) and ADR-0006 (stdout-only logging) creates a soft dependency on Railway's log capture model. If hosting ever moves, ADR-0006 needs to be revisited.

If any single ADR were reversed, the others would need re-evaluation. The decisions are coherent as a set, which is the test that an ADR compendium is doing real work and not just documenting choices made independently.
