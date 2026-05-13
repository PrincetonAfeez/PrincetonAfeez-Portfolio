# Contributing

This is a personal portfolio project, so the normal contribution path is private review rather than public feature requests.

Useful local commands:

```powershell
python manage.py migrate
python manage.py seed_apps
pytest
ruff check .
black --check .
djlint pages/templates portfolio/templates --check
```

Catalogue changes should be made in `content/apps.yaml`, not through the Django admin.
