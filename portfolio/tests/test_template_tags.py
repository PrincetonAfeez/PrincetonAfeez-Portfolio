"""Test template tags for the portfolio app."""

import pytest
from django.template import Context, Template

from portfolio.models import App


@pytest.mark.django_db
def test_doc_url_template_tag_wraps_model_method():
    app = App.objects.create(
        name="String Sanitizer",
        slug="string-sanitizer",
        short_description="Cleans text.",
        status="completed",
        build_order=1,
        github_url="https://github.com/PrincetonAfeez/String-Sanitizer",
        docs_url="https://github.com/PrincetonAfeez/String-Sanitizer/blob/main/string_sanitizer_docs.md",
    )
    template = Template("{% load doc_tags %}{% doc_url app 'ADR' %}")

    rendered = template.render(Context({"app": app}))

    assert rendered.endswith("string_sanitizer_docs.md#adr")
