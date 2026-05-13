"""Project URL configuration."""

from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import AppSitemap, StaticViewSitemap
from pages import views as page_views

sitemaps = {
    "static": StaticViewSitemap,
    "apps": AppSitemap,
}

urlpatterns = [
    path(f"{settings.ADMIN_URL_PREFIX.strip('/')}/", admin.site.urls),
    path("", include(("pages.urls", "pages"), namespace="pages")),
    path("apps/", include(("portfolio.urls", "portfolio"), namespace="portfolio")),
    path("resume.pdf", page_views.resume_pdf, name="resume_pdf"),
    path("robots.txt", page_views.robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
        *urlpatterns,
    ]

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
