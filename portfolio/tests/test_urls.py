"""Test URLs for the portfolio app."""

from django.urls import resolve, reverse


def test_app_list_route_resolves():
    match = resolve(reverse("portfolio:app_list"))

    assert match.view_name == "portfolio:app_list"


def test_app_detail_route_resolves():
    match = resolve(reverse("portfolio:app_detail", kwargs={"slug": "string-sanitizer"}))

    assert match.view_name == "portfolio:app_detail"
