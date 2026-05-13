"""Development settings."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]  # noqa: F405

_middleware = list(MIDDLEWARE)  # noqa: F405
_middleware.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE = _middleware

INTERNAL_IPS = ["127.0.0.1", "::1"]
