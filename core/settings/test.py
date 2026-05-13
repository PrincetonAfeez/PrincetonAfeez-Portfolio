"""Test-only Django settings.

``DJANGO_SETTINGS_MODULE`` must be ``core.settings.test`` (see ``pyproject.toml``
``[tool.pytest.ini_options]`` and CI). Do not use this module for ``runserver`` or
production: ``PASSWORD_HASHERS`` is set to MD5 for test speed.

Nothing imports this module; it is loaded only when that environment variable is
set for the test process. Application entrypoints default to ``dev`` (``manage.py``)
or ``prod`` (``wsgi`` / ``asgi``).
"""

from __future__ import annotations

import os

import dj_database_url

from .base import *  # noqa: F403

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

if os.environ.get("DATABASE_URL"):
    DATABASES = {"default": dj_database_url.config(conn_max_age=0)}

LOGGING = build_logging_config(is_prod=False)  # noqa: F405
