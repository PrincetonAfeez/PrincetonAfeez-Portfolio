"""Test template tags."""

from django.template import Context, Template
from django.test import RequestFactory


def render_active_link(path: str, route_name: str) -> str:
    request = RequestFactory().get(path)
    template = Template("{% load nav_tags %}{% active_link route_name %}")
    return template.render(Context({"request": request, "route_name": route_name}))


def test_active_link_returns_active_for_current_route():
    assert render_active_link("/apps/", "portfolio:app_list") == "active"


def test_active_link_returns_empty_for_other_route():
    assert render_active_link("/contact/", "portfolio:app_list") == ""
