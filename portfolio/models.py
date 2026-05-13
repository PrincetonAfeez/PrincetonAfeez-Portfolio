"""Portfolio catalogue models."""

from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Stack(models.Model):
    """A technology used in an app."""

    CATEGORY_CHOICES = [
        ("language", "Language"),
        ("framework", "Framework"),
        ("library", "Library"),
        ("tool", "Tool"),
        ("database", "Database"),
        ("service", "Service"),
    ]

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self) -> str:
        return self.name


class Concept(models.Model):
    """A concept or skill demonstrated by an app."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class App(models.Model):
    """A single app in the portfolio."""

    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("planned", "Planned"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    short_description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    build_order = models.PositiveIntegerField(unique=True, db_index=True)
    github_url = models.URLField()
    docs_url = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to="apps/", blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stack = models.ManyToManyField(Stack, related_name="apps", blank=True)
    concepts = models.ManyToManyField(Concept, related_name="apps", blank=True)

    DOC_ANCHORS = {
        "ADR": "adr",
        "TDD": "tdd",
        "IDS": "ids",
        "RUNBOOK": "runbook",
        "LESSONS_LEARNED": "lessons-learned",
    }

    class Meta:
        ordering = ["-build_order"]

    def __str__(self) -> str:
        return f"#{self.build_order} {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("portfolio:app_detail", kwargs={"slug": self.slug})

    @property
    def docs_filename(self) -> str:
        return f"{slugify(self.name).replace('-', '_')}_docs.md"

    def doc_url(self, doc_type: str) -> str:
        anchor = self.DOC_ANCHORS[doc_type]
        docs_url = self.docs_url or f"{self.github_url}/blob/main/{self.docs_filename}"
        return f"{docs_url}#{anchor}"
