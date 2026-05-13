# Content Intake

Use `content/apps.yaml` as the single source of truth for the app catalogue.

Preferred structure:

1. Define every stack item under `stacks`.
2. Define every concept under `concepts`.
3. Define every app under `apps`, referencing stack and concept slugs.

App fields:

- `name`: public display name.
- `slug`: URL slug, lowercase kebab-case.
- `short_description`: one sentence, 200 characters or less.
- `status`: `completed`, `in_progress`, or `planned`.
- `build_order`: integer sequence number.
- `github_url`: repository root URL, no trailing slash.
- `docs_url`: exact GitHub Markdown documentation file URL, without an anchor.
- `completed_date`: ISO date (`YYYY-MM-DD`) or blank for planned work.
- `stack`: list of stack slugs.
- `concepts`: list of concept slugs.

Stack fields:

- `name`: display name.
- `category`: one of `language`, `framework`, `library`, `tool`, `database`, or `service`.

Concept fields:

- `name`: display name.
- `description`: short explanation of the skill or idea.

This format gives the seed command enough information to create `Stack`, `Concept`, and `App` rows without guessing categories from slugs.

Use `github_url` for the visible "View on GitHub" source link. Use `docs_url` for the five documentation buttons. The site appends anchors such as `#adr`, `#tdd`, and `#lessons-learned` to `docs_url`.
