"""Playwright (sync) + Django live server fixtures for e2e and a11y tests."""

from __future__ import annotations

import os

import pytest
from django.core.management import call_command
from playwright.sync_api import sync_playwright


def pytest_collection_modifyitems(config, items):
    """Playwright uses asyncio; live_server + ORM need Django's escape hatch for tests."""
    if not items:
        return
    if any(_item_is_e2e(item) for item in items):
        os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


def _item_is_e2e(item) -> bool:
    path = getattr(item, "path", None) or getattr(item, "fspath", None)
    return path is not None and "e2e" in str(path)


@pytest.fixture
def page(live_server, seeded_catalogue):
    """Browser + page bound to ``live_server`` (seed DB before Playwright starts)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url=live_server.url)
        page = context.new_page()
        page.set_default_timeout(30_000)
        yield page
        context.close()
        browser.close()


@pytest.fixture(autouse=True)
def _e2e_debug_for_static_files(settings):
    """Serve static via runserver the same way as local dev (``find_files``)."""
    settings.DEBUG = True


@pytest.fixture
def seeded_catalogue(transactional_db):
    """Populate the catalogue for routes that list apps."""
    call_command("seed_apps")
