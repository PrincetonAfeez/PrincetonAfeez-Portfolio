"""Tests for production-only settings invariants."""

from __future__ import annotations

import importlib
import sys

import pytest
from django.core.exceptions import ImproperlyConfigured


def test_prod_requires_admin_allowed_ips(monkeypatch):
    """ADMIN_ALLOWED_IPS must be non-empty when loading core.settings.prod."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("SECRET_KEY", "x" * 60)
    monkeypatch.delenv("ADMIN_ALLOWED_IPS", raising=False)
    monkeypatch.setattr("core.settings.base.load_dotenv", lambda: None, raising=False)

    for name in ("core.settings.prod", "core.settings.base"):
        sys.modules.pop(name, None)

    with pytest.raises(ImproperlyConfigured, match="ADMIN_ALLOWED_IPS"):
        importlib.import_module("core.settings.prod")


def test_prod_loads_with_admin_allowed_ips(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("SECRET_KEY", "x" * 60)
    monkeypatch.setenv("ADMIN_ALLOWED_IPS", "127.0.0.1")
    monkeypatch.setattr("core.settings.base.load_dotenv", lambda: None, raising=False)

    for name in ("core.settings.prod", "core.settings.base"):
        sys.modules.pop(name, None)

    mod = importlib.import_module("core.settings.prod")
    assert mod.ADMIN_ALLOWED_IPS == ["127.0.0.1"]
