"""Sitemap definitions."""

from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from portfolio.models import App


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["pages:home", "pages:about", "pages:contact", "portfolio:app_list"]

    def location(self, item):
        return reverse(item)


class AppSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return App.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
