"""Admin for the portfolio app."""

from django.contrib import admin

from .models import App, Concept, Stack


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category")
    list_filter = ("category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ("build_order", "name", "status", "completed_date")
    list_filter = ("status", "stack", "concepts")
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("stack", "concepts")
    ordering = ("-build_order",)
