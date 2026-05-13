"""Template tags for navigation."""

from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, route_name: str) -> str:
    request = context.get("request")
    if request is None:
        return ""

    try:
        target = reverse(route_name)
    except NoReverseMatch:
        return ""

    current = request.path
    if target == "/":
        return "active" if current == target else ""
    return "active" if current.startswith(target) else ""
