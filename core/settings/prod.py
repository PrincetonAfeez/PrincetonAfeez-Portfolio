"""Production settings."""

from __future__ import annotations

import os

import dj_database_url
import sentry_sdk
from csp.constants import NONE, SELF
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = env_csv("ALLOWED_HOSTS", "princetonafeez.com,www.princetonafeez.com")  # noqa: F405

if not ADMIN_ALLOWED_IPS:  # noqa: F405
    raise ImproperlyConfigured(
        "ADMIN_ALLOWED_IPS must be set in production "
        "(comma-separated IPs allowed to reach Django admin)."
    )

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Manifest staticfiles storage is only configured here (not in base.py), so local
# dev keeps Django defaults. Smoke-test once before deploy: prod settings +
# collectstatic + runserver against Postgres surfaces missing-asset manifest errors
# before Railway does.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# After WhiteNoise so CSP headers are also applied to static asset responses (django-csp guidance).
MIDDLEWARE.insert(2, "csp.middleware.CSPMiddleware")  # noqa: F405

INSTALLED_APPS = [*INSTALLED_APPS, "csp"]  # noqa: F405

SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

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

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

LOGGING = build_logging_config(is_prod=True)  # noqa: F405
