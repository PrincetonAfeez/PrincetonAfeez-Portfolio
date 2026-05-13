"""Views for the app catalogue."""

from __future__ import annotations

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import App

PAGE_SIZE = 10


def app_list(request):
    apps_qs = App.objects.prefetch_related("stack", "concepts").order_by("-build_order")
    paginator = Paginator(apps_qs, PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page", 1))

    context = {
        "apps": page.object_list,
        "page": page,
        "has_next": page.has_next(),
        "next_page": page.next_page_number() if page.has_next() else None,
        "total_apps": paginator.count,
    }

    if request.headers.get("HX-Request"):
        return render(request, "portfolio/partials/app_list_page.html", context)
    return render(request, "portfolio/app_list.html", context)


def app_detail(request, slug: str):
    app = get_object_or_404(
        App.objects.prefetch_related("stack", "concepts"),
        slug=slug,
    )
    return render(request, "portfolio/app_detail.html", {"app": app})
