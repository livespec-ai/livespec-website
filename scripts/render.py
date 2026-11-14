"""Render content/**/*.md to site/**/*.html with pandoc (run via `just render`).

Implements the render command in SPECIFICATION/non-functional-requirements.md:
each Markdown source becomes the page at the same relative path under site/
(.md -> .html), through the one shared template templates/page.html.
Rendered pages are gitignored build output: `just check` and the deploy
workflow both render before using site/, and every render first removes
the previously rendered pages so a deleted source leaves no stale page.

Front matter keys: title (the <title> text), description, and, for blog
entries, layout: article, heading and published (YYYY-MM-DD). The 404 page
sets root_absolute: true so its links are root-absolute (SPECIFICATION/contracts.md,
URL surface); every other page links by the shortest relative path.
"""

from __future__ import annotations

import datetime
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"
TEMPLATE = ROOT / "templates" / "page.html"
ORIGIN = "https://livespec-ai.org"
READER = "gfm-gfm_auto_identifiers+attributes"


def pandoc(*args: str, stdin: str) -> str:
    try:
        return subprocess.run(
            ["pandoc", *args], input=stdin, capture_output=True, text=True, check=True
        ).stdout
    except FileNotFoundError:
        sys.exit("render: pandoc not found; run `just bootstrap`, then run through `mise exec --`")


def front_matter(source: str) -> dict[str, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tpl:
        tpl.write("$meta-json$")
    try:
        out = pandoc(f"--from={READER}", "--to=plain", "--wrap=none",
                     f"--template={tpl.name}", stdin=source)
    finally:
        os.unlink(tpl.name)
    return json.loads(out)


def attr(value: str) -> str:
    """Escape for a double-quoted attribute, leaving apostrophes as-is like the hand-authored pages."""
    return html.escape(value, quote=False).replace('"', "&quot;")


def href(page: Path, target: str, absolute: bool) -> str:
    """Link from site page `page` (relative to site/) to `target` (relative to site/)."""
    if absolute:
        return "/" + target.removesuffix("index.html")
    return os.path.relpath(target, page.parent.as_posix() or ".")


def render_page(src: Path) -> tuple[Path, str]:
    """Return (page path relative to site/, rendered HTML) for one Markdown source."""
    page = src.relative_to(CONTENT).with_suffix(".html")
    source = src.read_text()
    meta = front_matter(source)
    absolute = meta.get("root_absolute") is True
    path = "/" + page.as_posix().removesuffix("index.html")
    variables = {
        "page-title": meta["title"],
        "page-description": meta["description"],
        "canonical-url": ORIGIN + path,
        "url-path": path,
        "css-href": href(page, "css/style.css", absolute),
        "home-href": href(page, "index.html", absolute),
        "blog-href": href(page, "blog/index.html", absolute),
    }
    if meta.get("layout") == "article":
        published = datetime.date.fromisoformat(meta["published"])
        variables |= {
            "article": "true",
            "page-heading": meta["heading"],
            "published": published.isoformat(),
            "published-display": f"{published:%B} {published.day}, {published.year}",
        }
    args = [f"--from={READER}", "--to=html5", "--wrap=none", f"--template={TEMPLATE}"]
    args += [f"--variable={k}={attr(v)}" for k, v in variables.items()]
    return page, pandoc(*args, stdin=source)


def sources() -> list[Path]:
    return sorted(CONTENT.rglob("*.md"))


def render_all(out_dir: Path) -> list[Path]:
    """Render every source into out_dir; return the page paths relative to out_dir."""
    pages = []
    for src in sources():
        page, rendered = render_page(src)
        (out_dir / page).parent.mkdir(parents=True, exist_ok=True)
        (out_dir / page).write_text(rendered)
        pages.append(page)
    return pages


def clean(out_dir: Path) -> None:
    """Remove every previously rendered page; all HTML under site/ is rendered output."""
    for page in out_dir.rglob("*.html"):
        page.unlink()


def main() -> int:
    clean(SITE)
    pages = render_all(SITE)
    print(f"render: {len(pages)} pages rendered from content/ into site/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
