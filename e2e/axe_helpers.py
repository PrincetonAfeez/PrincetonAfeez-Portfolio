"""Helpers for axe-core runs inside Playwright."""

from __future__ import annotations

from pathlib import Path

import pytest

SITE_ROOT = Path(__file__).resolve().parents[1]


def axe_core_path() -> Path:
    path = SITE_ROOT / "node_modules" / "axe-core" / "axe.min.js"
    if not path.is_file():
        pytest.skip("axe-core not installed (run npm ci)")
    return path


def run_axe(page, axe_path: Path) -> dict:
    page.add_script_tag(path=str(axe_path))
    return page.evaluate(
        "() => axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag21a'] } })"
    )


def format_violations(violations: list) -> str:
    lines = []
    for v in violations:
        rules = ", ".join(r.get("target", r.get("html", "?")) for r in v.get("nodes", [])[:3])
        lines.append(
            f"- {v.get('id')} ({v.get('impact')}): {v.get('description', '')[:120]} … {rules}"
        )
    return "\n".join(lines)
