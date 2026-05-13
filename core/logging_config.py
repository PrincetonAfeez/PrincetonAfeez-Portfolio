"""Logging configuration helpers."""

from __future__ import annotations


def build_logging_config(is_prod: bool) -> dict:
    """Return a Django LOGGING dict for development or production."""

    formatter = "json" if is_prod else "human"
    app_level = "INFO" if is_prod else "DEBUG"
    django_level = "WARNING" if is_prod else "INFO"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "human": {
                "format": "%(asctime)s %(levelname)-8s %(name)s %(message)s",
            },
            "json": {
                "()": "pythonjsonlogger.json.JsonFormatter",
                "format": (
                    "%(asctime)s %(levelname)s %(name)s %(message)s "
                    "%(module)s %(funcName)s %(lineno)d %(pathname)s"
                ),
                "rename_fields": {
                    "asctime": "timestamp",
                    "levelname": "level",
                    "name": "logger",
                },
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": formatter,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": django_level,
                "propagate": False,
            },
            "pages": {
                "handlers": ["console"],
                "level": app_level,
                "propagate": False,
            },
            "portfolio": {
                "handlers": ["console"],
                "level": app_level,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
