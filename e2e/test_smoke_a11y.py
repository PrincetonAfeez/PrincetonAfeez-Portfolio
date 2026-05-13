"""Browser smoke tests and axe-core accessibility scans (WCAG 2 A / 2.1 A tags)."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from e2e.axe_helpers import axe_core_path, format_violations, run_axe

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def axe_core_js():
    return axe_core_path()


def test_home_smoke(page, live_server):
    page.goto("/", wait_until="domcontentloaded")
    expect(page.locator("#main")).to_be_visible()
    expect(page.get_by_role("link", name="Skip to content")).to_be_attached()


def test_apps_catalogue_smoke(page, live_server):
    page.goto("/apps/", wait_until="domcontentloaded")
    expect(page.locator("#app-list")).to_be_visible()
    expect(page.locator("#app-list")).to_have_attribute("aria-live", "polite")
    expect(page.get_by_text("Plate Validator", exact=False).first).to_be_visible()


def test_home_axe_no_critical_or_serious_violations(page, live_server, axe_core_js):
    page.goto("/", wait_until="networkidle")
    result = run_axe(page, axe_core_js)
    bad = [v for v in result.get("violations", []) if v.get("impact") in ("critical", "serious")]
    assert not bad, "axe violations (critical/serious):\n" + format_violations(bad)


def test_apps_list_axe_no_critical_or_serious_violations(page, live_server, axe_core_js):
    page.goto("/apps/", wait_until="networkidle")
    result = run_axe(page, axe_core_js)
    bad = [v for v in result.get("violations", []) if v.get("impact") in ("critical", "serious")]
    assert not bad, "axe violations (critical/serious):\n" + format_violations(bad)
