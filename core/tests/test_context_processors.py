"""Tests for ``core.context_processors``."""

from __future__ import annotations

import pytest
from django.test import RequestFactory

from core.context_processors import site_context


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.parametrize(
    ("allowed_hosts", "expected_domain"),
    [
        (["www.example.com"], "example.com"),
        (["example.com"], "example.com"),
        (["*", "localhost", "127.0.0.1"], "localhost"),
    ],
)
def test_site_context_domain_from_allowed_hosts(settings, rf, allowed_hosts, expected_domain):
    settings.ALLOWED_HOSTS = list(allowed_hosts)
    request = rf.get("/")
    assert site_context(request)["SITE_DOMAIN"] == expected_domain
