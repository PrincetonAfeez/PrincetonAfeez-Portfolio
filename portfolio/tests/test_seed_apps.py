"""Test seed_apps command."""

import pytest
from django.core.management import call_command

from portfolio.models import App, Concept, Stack


@pytest.mark.django_db
def test_seed_apps_creates_manifest_content():
    call_command("seed_apps")

    assert App.objects.count() == 40
    assert Stack.objects.count() == 14
    assert Concept.objects.count() == 91
    assert App.objects.get(slug="string-sanitizer").docs_url.endswith("string_sanitizer_docs.md")


@pytest.mark.django_db
def test_seed_apps_is_idempotent():
    call_command("seed_apps")
    call_command("seed_apps")

    assert App.objects.count() == 40
    assert App.objects.get(build_order=40).slug == "plate-validator"
