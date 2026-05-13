"""Seed portfolio app metadata from content/apps.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from portfolio.models import App, Concept, Stack


class Command(BaseCommand):
    help = "Seed Stack, Concept, and App rows from content/apps.yaml."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=settings.BASE_DIR / "content" / "apps.yaml",
            help="Path to the YAML manifest.",
        )

    def handle(self, *args, **options):
        manifest_path = Path(options["path"])
        if not manifest_path.exists():
            raise CommandError(f"Manifest not found: {manifest_path}")

        with manifest_path.open(encoding="utf-8") as manifest_file:
            manifest = yaml.safe_load(manifest_file) or {}

        stacks = manifest.get("stacks") or {}
        concepts = manifest.get("concepts") or {}
        apps = manifest.get("apps") or []

        stack_objects = {}
        for slug, data in stacks.items():
            stack, _ = Stack.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": data["name"],
                    "category": data["category"],
                },
            )
            stack_objects[slug] = stack

        concept_objects = {}
        for slug, data in concepts.items():
            concept, _ = Concept.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": data["name"],
                    "description": data.get("description", ""),
                },
            )
            concept_objects[slug] = concept

        for row in apps:
            missing_stacks = sorted(set(row.get("stack", [])) - set(stack_objects))
            missing_concepts = sorted(set(row.get("concepts", [])) - set(concept_objects))
            if missing_stacks or missing_concepts:
                raise CommandError(
                    f"{row.get('name', row.get('slug'))} references missing taxonomy: "
                    f"stacks={missing_stacks}, concepts={missing_concepts}"
                )

            app, _ = App.objects.update_or_create(
                slug=row["slug"],
                defaults={
                    "name": row["name"],
                    "short_description": row["short_description"],
                    "status": row["status"],
                    "build_order": row["build_order"],
                    "github_url": row["github_url"],
                    "docs_url": row.get("docs_url", ""),
                    "completed_date": row.get("completed_date") or None,
                },
            )
            app.stack.set(stack_objects[slug] for slug in row.get("stack", []))
            app.concepts.set(concept_objects[slug] for slug in row.get("concepts", []))

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(stack_objects)} stacks, {len(concept_objects)} concepts, "
                f"and {len(apps)} apps."
            )
        )
