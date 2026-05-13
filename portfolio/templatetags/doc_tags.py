"""Template tags for the portfolio app."""

from django import template

register = template.Library()


@register.simple_tag
def doc_url(app, doc_type: str) -> str:
    return app.doc_url(doc_type)
