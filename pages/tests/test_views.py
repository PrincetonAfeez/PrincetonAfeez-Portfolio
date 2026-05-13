"""Test views."""

from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

from pages.views import server_error


def test_home_view_renders_positioning_line(client):
    response = client.get(reverse("pages:home"))

    assert response.status_code == 200
    assert b"35 years operating restaurants" in response.content
    assert b"View my technical work" in response.content


def test_contact_view_renders_contact_links(client):
    response = client.get(reverse("pages:contact"))

    assert response.status_code == 200
    assert b"mailto:princetonafeez@gmail.com" in response.content
    assert b"https://www.linkedin.com/in/princetonai/" in response.content


def test_about_view_renders(client):
    response = client.get(reverse("pages:about"))

    assert response.status_code == 200
    assert b"From Lagos to London to Los Angeles" in response.content


def test_robots_txt_excludes_admin(client, settings):
    settings.ADMIN_URL_PREFIX = "control-test"

    response = client.get(reverse("robots"))

    assert response.status_code == 200
    body = response.content.decode()
    assert "Disallow: /control-test/" in body
    assert "Sitemap: http://testserver/sitemap.xml" in body


def test_resume_pdf_route_serves_file(client):
    response = client.get(reverse("resume_pdf"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert "inline" in response["Content-Disposition"]
    assert "resume.pdf" in response["Content-Disposition"]


def test_resume_pdf_returns_404_when_file_missing(client, monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "BASE_DIR", tmp_path)
    response = client.get(reverse("resume_pdf"))
    assert response.status_code == 404


def test_custom_404_handler_renders_template(client):
    response = client.get("/this-route-does-not-exist-404/")
    assert response.status_code == 404
    assert b"That page is not on the floor plan" in response.content


def test_server_error_view_returns_500():
    request = RequestFactory().get("/")
    response = server_error(request)
    assert response.status_code == 500
    assert b"500" in response.content
