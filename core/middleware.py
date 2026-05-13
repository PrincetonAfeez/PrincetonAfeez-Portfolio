"""Project middleware."""

from __future__ import annotations

from django.conf import settings
from django.http import Http404


class AdminIPAllowlistMiddleware:
    """Return 404 for admin requests outside the configured allowlist."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_prefix = f"/{settings.ADMIN_URL_PREFIX.strip('/')}/"
        allowed_ips = set(getattr(settings, "ADMIN_ALLOWED_IPS", []))

        if allowed_ips and request.path.startswith(admin_prefix):
            forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
            client_ip = forwarded_for.split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")
            if client_ip not in allowed_ips:
                raise Http404

        return self.get_response(request)
