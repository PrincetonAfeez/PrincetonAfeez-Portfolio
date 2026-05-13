"""Test views for the portfolio app."""

import pytest
from django.core.management import call_command
from django.urls import reverse


@pytest.fixture
def seeded_apps(db):
    call_command("seed_apps")


@pytest.mark.django_db
def test_app_list_full_page(client, seeded_apps):
    response = client.get(reverse("portfolio:app_list"))

    assert response.status_code == 200
    assert b"Plate Validator" in response.content
    assert b"App #40 of 40" in response.content
    assert b'id="app-list"' in response.content
    assert b'aria-live="polite"' in response.content


@pytest.mark.django_db
def test_app_list_hx_request_returns_partial(client, seeded_apps):
    response = client.get(reverse("portfolio:app_list"), headers={"HX-Request": "true"})

    assert response.status_code == 200
    assert b"app-card" in response.content
    assert b"<!doctype html>" not in response.content.lower()


@pytest.mark.django_db
def test_app_list_pagination_page_two(client, seeded_apps):
    response = client.get(reverse("portfolio:app_list"), {"page": 2})

    assert response.status_code == 200
    assert b"Vault OS" in response.content


@pytest.mark.django_db
def test_app_detail_existing_slug(client, seeded_apps):
    response = client.get(reverse("portfolio:app_detail", kwargs={"slug": "string-sanitizer"}))

    assert response.status_code == 200
    assert b"String Sanitizer" in response.content
    assert b"#lessons-learned" in response.content
    assert b'href="/static/css/site.css"' in response.content
    assert b'href="/static/css/tw-compiled.css"' in response.content


@pytest.mark.django_db
def test_app_detail_missing_slug_returns_404(client, seeded_apps):
    response = client.get(reverse("portfolio:app_detail", kwargs={"slug": "missing"}))

    assert response.status_code == 404
