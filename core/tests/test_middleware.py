"""Tests for ``core.middleware``."""

from __future__ import annotations

import pytest
from django.http import Http404, HttpResponse
from django.test import RequestFactory, override_settings

from core.middleware import AdminIPAllowlistMiddleware


@pytest.fixture
def rf():
    return RequestFactory()


def test_admin_ip_middleware_noop_when_allowlist_empty(rf, settings):
    settings.ADMIN_URL_PREFIX = "secret-admin"
    settings.ADMIN_ALLOWED_IPS = []
    mw = AdminIPAllowlistMiddleware(lambda req: HttpResponse(b"ok"))

    request = rf.get("/secret-admin/login/")
    assert mw(request).content == b"ok"


@override_settings(ADMIN_URL_PREFIX="ctrl", ADMIN_ALLOWED_IPS=["127.0.0.1"])
def test_admin_ip_middleware_allows_listed_remote_addr(rf):
    mw = AdminIPAllowlistMiddleware(lambda req: HttpResponse(b"ok"))
    request = rf.get("/ctrl/login/", REMOTE_ADDR="127.0.0.1")
    assert mw(request).content == b"ok"


@override_settings(ADMIN_URL_PREFIX="ctrl", ADMIN_ALLOWED_IPS=["127.0.0.1"])
def test_admin_ip_middleware_blocks_unlisted_remote_addr(rf):
    mw = AdminIPAllowlistMiddleware(lambda req: HttpResponse(b"ok"))
    request = rf.get("/ctrl/login/", REMOTE_ADDR="198.51.100.2")
    with pytest.raises(Http404):
        mw(request)


@override_settings(ADMIN_URL_PREFIX="ctrl", ADMIN_ALLOWED_IPS=["203.0.113.5"])
def test_admin_ip_middleware_prefers_x_forwarded_for_first_hop(rf):
    mw = AdminIPAllowlistMiddleware(lambda req: HttpResponse(b"ok"))
    request = rf.get("/ctrl/", REMOTE_ADDR="10.0.0.1")
    request.META["HTTP_X_FORWARDED_FOR"] = "203.0.113.5, 10.0.0.2"
    assert mw(request).content == b"ok"


@override_settings(ADMIN_URL_PREFIX="ctrl", ADMIN_ALLOWED_IPS=["127.0.0.1"])
def test_admin_ip_middleware_non_admin_paths_ignore_allowlist(rf):
    mw = AdminIPAllowlistMiddleware(lambda req: HttpResponse(b"ok"))
    request = rf.get("/apps/", REMOTE_ADDR="198.51.100.9")
    assert mw(request).content == b"ok"
