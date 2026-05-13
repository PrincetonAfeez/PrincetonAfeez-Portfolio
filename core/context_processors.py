"""Site-wide template context."""

from __future__ import annotations

from django.conf import settings


def _primary_site_domain(allowed_hosts: list[str] | tuple[str, ...]) -> str:
    """Pick a display hostname from ALLOWED_HOSTS (skips wildcards and loopback)."""

    for raw in allowed_hosts:
        host = raw.strip() if isinstance(raw, str) else str(raw).strip()
        if not host or host == "*":
            continue
        if host in {"localhost", "127.0.0.1", "[::1]"}:
            continue
        if host.startswith("www."):
            return host[4:]
        return host
    return "localhost"


def site_context(request):
    """Expose stable site metadata to templates."""

    return {
        "SITE_NAME": "Princeton Afeez",
        "SITE_DOMAIN": _primary_site_domain(getattr(settings, "ALLOWED_HOSTS", [])),
        "SITE_VERSION": settings.SITE_VERSION,
        "CONTACT_EMAIL": "princetonafeez@gmail.com",
        "LINKEDIN_URL": "https://www.linkedin.com/in/princetonai/",
        "GITHUB_URL": "https://github.com/PrincetonAfeez",
        "RESUME_URL": "/resume.pdf",
        "NAV_ITEMS": [
            ("pages:home", "Home"),
            ("portfolio:app_list", "Apps"),
            ("pages:contact", "Contact"),
        ],
    }
