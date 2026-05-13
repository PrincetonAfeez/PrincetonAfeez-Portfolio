"""Initial migrations for the portfolio app."""

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Concept",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Stack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(max_length=50, unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("language", "Language"),
                            ("framework", "Framework"),
                            ("library", "Library"),
                            ("tool", "Tool"),
                            ("database", "Database"),
                            ("service", "Service"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
            options={"ordering": ["category", "name"]},
        ),
        migrations.CreateModel(
            name="App",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=120, unique=True)),
                ("short_description", models.CharField(max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("completed", "Completed"),
                            ("in_progress", "In Progress"),
                            ("planned", "Planned"),
                        ],
                        max_length=20,
                    ),
                ),
                ("build_order", models.PositiveIntegerField(db_index=True, unique=True)),
                ("github_url", models.URLField()),
                ("docs_url", models.URLField(blank=True)),
                ("hero_image", models.ImageField(blank=True, null=True, upload_to="apps/")),
                ("completed_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "concepts",
                    models.ManyToManyField(blank=True, related_name="apps", to="portfolio.concept"),
                ),
                (
                    "stack",
                    models.ManyToManyField(blank=True, related_name="apps", to="portfolio.stack"),
                ),
            ],
            options={"ordering": ["-build_order"]},
        ),
    ]
