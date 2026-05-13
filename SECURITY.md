# Security

This portfolio has no user accounts, public forms, comments, uploads, or public API in v1.

Production hardening includes:

- `DEBUG=False`
- randomized admin URL via `ADMIN_URL_PREFIX`
- admin IP allowlist via `ADMIN_ALLOWED_IPS` (required in production settings; unset or empty prevents startup)
- secure cookies
- HSTS
- `X_FRAME_OPTIONS=DENY`
- `SECURE_CONTENT_TYPE_NOSNIFF=True`
- strict referrer policy
- Content Security Policy in production

Report issues directly to `princetonafeez@gmail.com`.
