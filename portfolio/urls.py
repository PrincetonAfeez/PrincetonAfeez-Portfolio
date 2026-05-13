"""URLs for the portfolio app."""

from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.app_list, name="app_list"),
    path("<slug:slug>/", views.app_detail, name="app_detail"),
]
