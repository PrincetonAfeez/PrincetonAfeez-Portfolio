"""Test models for the portfolio app."""

import pytest

from portfolio.models import App


@pytest.mark.django_db
def test_docs_filename_uses_snake_case():
    app = App.objects.create(
        name="String Sanitizer",
        slug="string-sanitizer",
        short_description="Cleans text.",
        status="completed",
        build_order=1,
        github_url="https://github.com/PrincetonAfeez/String-Sanitizer",
    )

    assert app.docs_filename == "string_sanitizer_docs.md"


@pytest.mark.django_db
def test_doc_url_uses_exact_docs_url_when_present():
    app = App.objects.create(
        name="String Sanitizer",
        slug="string-sanitizer",
        short_description="Cleans text.",
        status="completed",
        build_order=1,
        github_url="https://github.com/PrincetonAfeez/String-Sanitizer",
        docs_url="https://github.com/PrincetonAfeez/String-Sanitizer/blob/main/string_sanitizer_docs.md",
    )

    assert app.doc_url("ADR") == (
        "https://github.com/PrincetonAfeez/String-Sanitizer/blob/main/"
        "string_sanitizer_docs.md#adr"
    )
    assert app.doc_url("LESSONS_LEARNED").endswith("#lessons-learned")


@pytest.mark.django_db
def test_doc_url_falls_back_to_default_filename():
    app = App.objects.create(
        name="CSV Converter",
        slug="csv-converter",
        short_description="Converts CSV.",
        status="completed",
        build_order=4,
        github_url="https://github.com/PrincetonAfeez/CSV-Converter",
    )

    assert app.doc_url("TDD") == (
        "https://github.com/PrincetonAfeez/CSV-Converter/blob/main/csv_converter_docs.md#tdd"
    )


@pytest.mark.django_db
def test_doc_url_invalid_key_raises_key_error():
    app = App.objects.create(
        name="CSV Converter",
        slug="csv-converter",
        short_description="Converts CSV.",
        status="completed",
        build_order=4,
        github_url="https://github.com/PrincetonAfeez/CSV-Converter",
    )

    with pytest.raises(KeyError):
        app.doc_url("NOPE")


@pytest.mark.django_db
def test_get_absolute_url():
    app = App.objects.create(
        name="CSV Converter",
        slug="csv-converter",
        short_description="Converts CSV.",
        status="completed",
        build_order=4,
        github_url="https://github.com/PrincetonAfeez/CSV-Converter",
    )

    assert app.get_absolute_url() == "/apps/csv-converter/"
