"""Views for static marketing pages."""

from __future__ import annotations

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .content import CAPABILITIES, CERTIFICATIONS, EDUCATION, OPERATOR_STACK, WORK_HISTORY


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "work_history": WORK_HISTORY,
            "capabilities": CAPABILITIES,
            "operator_stack": OPERATOR_STACK,
            "certifications": CERTIFICATIONS,
            "education": EDUCATION,
        },
    )


def about(request):
    return render(
        request,
        "pages/about.html",
        {
            "work_history": WORK_HISTORY,
            "capabilities": CAPABILITIES,
            "operator_stack": OPERATOR_STACK,
        },
    )


def contact(request):
    return render(request, "pages/contact.html")


def resume_pdf(request):
    resume_path = settings.BASE_DIR / "static" / "resume" / "resume.pdf"
    if not resume_path.is_file():
        raise Http404("Resume not available.")
    response = FileResponse(resume_path.open("rb"), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="resume.pdf"'
    return response


def robots_txt(request):
    admin_prefix = settings.ADMIN_URL_PREFIX.strip("/")
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Disallow: /{admin_prefix}/",
        f"Sitemap: {sitemap_url}",
    ]
    content = "\n".join(lines) + "\n"
    return HttpResponse(content, content_type="text/plain")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)
