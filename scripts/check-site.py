"""Check the publishable site under site/ (run via `just check`).

Implements the check-aggregate command in
SPECIFICATION/non-functional-requirements.md: HTML validity, a site-wide link check, the per-page contract
check from SPECIFICATION/contracts.md. `just check` renders the pages first, so this checks
exactly what a deploy of the same commit would publish. Exits 1 on any failure.

External links: 404/410 fail; 403/429, timeouts and network errors are
reported as unverified (not failures). Set SITE_CHECK_OFFLINE=1 to skip
external requests.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

import html5lib


ORIGIN = "https://livespec-ai.org"
SITE = Path(__file__).resolve().parent.parent / "site"
GOATCOUNTER = "https://livespec-ai.goatcounter.com/count"
FOOTER_LINKS = {"/", "/blog/", "https://github.com/thewoolleyman/livespec", "https://thewoolleyweb.com/"}
AUTHOR = "Chad Woolley"
AUTHOR_URL = "https://thewoolleyweb.com/"
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")

failures: list[str] = []
unverified: list[str] = []


def fail(page: str, msg: str) -> None:
    failures.append(f"{page}: {msg}")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.refs: list[str] = []
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.anchors: list[str] = []
        self.footer_hrefs: set[str] = set()
        self.header_hrefs: set[str] = set()
        self.times: list[str] = []
        self.tags: list[str] = []
        self.article_header_h1 = False
        self.lang = ""
        self.title = ""
        self._in_title = False
        self._div_stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1" and self.tags[-2:] == ["article", "header"]:
            self.article_header_h1 = True
        if tag in ("article", "header"):
            self.tags.append(tag)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "div":
            self._div_stack.append(a.get("id", ""))
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
            if "charset" in a:
                self.meta["charset"] = a["charset"]
        if tag == "link":
            self.links.append(a)
        if tag == "script":
            self.scripts.append(a)
        if tag == "time":
            self.times.append(a.get("datetime", ""))
        for attr in ("href", "src"):
            if attr in a and tag != "link" or (tag == "link" and attr == "href" and a.get("rel") == "stylesheet"):
                if attr in a:
                    self.refs.append(a[attr])
        if tag == "a" and "href" in a:
            self.anchors.append(a["href"])
            if "footer" in self._div_stack:
                self.footer_hrefs.add(a["href"])
            if "header" in self._div_stack:
                self.header_hrefs.add(a["href"])

    def handle_endtag(self, tag):
        if tag == "div" and self._div_stack:
            self._div_stack.pop()
        if tag in ("article", "header") and self.tags:
            self.tags.pop()
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def site_url(upath: str, href: str) -> str:
    """Resolve href from upath; internal targets become /dir/ URL paths."""
    absolute = urldefrag(urljoin(ORIGIN + upath, href))[0]
    if not absolute.startswith(ORIGIN + "/"):
        return href
    path = urlparse(absolute).path
    return path[: -len("index.html")] if path.endswith("/index.html") else path


def url_path(file: Path) -> str:
    rel = file.relative_to(SITE).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve_local(path: str) -> Path | None:
    target = SITE / unquote(path).lstrip("/")
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target if target.is_file() else None


def main() -> int:
    pages: dict[str, Page] = {}
    external: dict[str, set[str]] = {}
    html_files = sorted(SITE.rglob("*.html"))
    for file in html_files:
        upath = url_path(file)
        text = file.read_text(encoding="utf-8")
        if not text.startswith("<!DOCTYPE html>"):
            fail(upath, "must start with <!DOCTYPE html>")
        try:
            html5lib.HTMLParser(strict=True).parse(text)
        except html5lib.html5parser.ParseError as exc:
            fail(upath, f"invalid HTML5: {exc}")
        page = Page()
        page.feed(text)
        pages[upath] = page
        # Per-page contract (SPECIFICATION/contracts.md).
        if page.lang != "en":
            fail(upath, '<html lang="en"> required')
        if page.meta.get("charset", "").lower() != "utf-8":
            fail(upath, '<meta charset="utf-8"> required')
        if "width=device-width" not in page.meta.get("viewport", ""):
            fail(upath, "viewport meta required")
        canon = [l.get("href") for l in page.links if l.get("rel") == "canonical"]
        if canon != [ORIGIN + upath]:
            fail(upath, f"canonical must be {ORIGIN + upath}, got {canon}")
        if page.meta.get("og:url") != ORIGIN + upath:
            fail(upath, "og:url must equal the canonical URL")
        for key in ("description", "og:title", "og:description", "og:type"):
            if not page.meta.get(key):
                fail(upath, f"missing meta {key}")
        sheets = [l.get("href") for l in page.links if l.get("rel") == "stylesheet"]
        # Relative so pages render from file:// for local review; /404.html
        # stays absolute because Pages serves it at arbitrary paths.
        depth = len(file.relative_to(SITE).parts) - 1
        want_sheet = "/css/style.css" if upath == "/404.html" else "../" * depth + "css/style.css"
        if sheets != [want_sheet]:
            fail(upath, f"stylesheet must be exactly {want_sheet}, got {sheets}")
        gc = [s for s in page.scripts if s.get("data-goatcounter") == GOATCOUNTER]
        if not gc or "async" not in gc[0]:
            fail(upath, "missing async GoatCounter count.js script")
        if f"{GOATCOUNTER}?p={upath}" not in page.refs:
            fail(upath, "missing GoatCounter <noscript> pixel for this path")
        if "/" not in {site_url(upath, h) for h in page.header_hrefs}:
            fail(upath, "header must link the site title to /")
        footer = {site_url(upath, h) for h in page.footer_hrefs}
        if not FOOTER_LINKS <= footer:
            fail(upath, f"footer missing links: {sorted(FOOTER_LINKS - footer)}")
        # Internal links are relative and name index.html so pages navigate
        # from file://; /404.html links absolutely (Pages serves it anywhere).
        for href in page.anchors:
            if href.startswith(SKIP_SCHEMES) or href.startswith(("http:", "https:", "#")):
                continue
            target = urldefrag(href)[0]
            if upath == "/404.html":
                if not target.startswith("/"):
                    fail(upath, f"404 page links must be root-absolute: {href}")
            elif target.startswith("/") or not target.endswith(".html"):
                fail(upath, f"internal link must be relative and end in .html: {href}")
        is_entry = upath.startswith("/blog/") and upath != "/blog/"
        want_type = "article" if is_entry else "website"
        if page.meta.get("og:type") != want_type:
            fail(upath, f"og:type must be {want_type}")
        if is_entry:
            pub = page.meta.get("article:published_time", "")
            if not pub or pub not in page.times:
                fail(upath, "blog entry needs article:published_time matching a <time datetime>")
            if not page.article_header_h1:
                fail(upath, "blog entry needs an <article><header><h1> title")
            if page.meta.get("author") != AUTHOR:
                fail(upath, f'blog entry needs <meta name="author" content="{AUTHOR}">')
            if page.meta.get("article:author") != AUTHOR_URL:
                fail(upath, f"blog entry needs article:author {AUTHOR_URL}")
        # Collect references.
        for ref in page.refs:
            if ref.startswith(SKIP_SCHEMES):
                continue
            absolute = urljoin(ORIGIN + upath, ref)
            base, frag = urldefrag(absolute)
            if base.startswith(ORIGIN + "/") or base == ORIGIN:
                local = urlparse(base).path or "/"
                if local == "/count":
                    continue
                target = resolve_local(local)
                if target is None:
                    fail(upath, f"broken internal link {ref}")
                elif frag and target.suffix == ".html":
                    tp = Page()
                    tp.feed(target.read_text(encoding="utf-8"))
                    if frag not in tp.ids:
                        fail(upath, f"broken fragment {ref}")
            elif base.startswith(("http://", "https://")):
                external.setdefault(base, set()).add(upath)

    # Unique titles and descriptions.
    for key in ("title", "description"):
        seen: dict[str, str] = {}
        for upath, page in pages.items():
            value = page.title.strip() if key == "title" else page.meta.get("description", "")
            if not value:
                fail(upath, f"missing {key}")
            elif value in seen:
                fail(upath, f"{key} duplicates {seen[value]}")
            seen[value] = upath

    # Blog index lists every entry.
    entries = {p for p in pages if p.startswith("/blog/") and p != "/blog/"}
    blog_index = pages.get("/blog/")
    if blog_index is None:
        fail("/blog/", "blog index missing")
    else:
        missing = entries - {site_url("/blog/", r) for r in blog_index.refs}
        if missing:
            fail("/blog/", f"blog index missing entries {sorted(missing)}")

    # Sitemap lists exactly the published pages except 404.
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITE / "sitemap.xml")
    locs = {}
    for url in tree.getroot().findall("s:url", ns):
        loc = url.findtext("s:loc", namespaces=ns)
        lastmod = url.findtext("s:lastmod", namespaces=ns)
        locs[loc] = lastmod
        if not lastmod:
            fail("/sitemap.xml", f"{loc} missing lastmod")
    expected = {ORIGIN + p for p in pages if p != "/404.html"}
    if set(locs) != expected:
        fail("/sitemap.xml", f"must list exactly {sorted(expected)}, got {sorted(locs)}")
    robots = (SITE / "robots.txt").read_text()
    if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
        fail("/robots.txt", "must reference the sitemap")
    if (SITE / "CNAME").read_text().strip() != "livespec-ai.org":
        fail("/CNAME", "must contain livespec-ai.org")
    if not (SITE / ".nojekyll").exists():
        fail("/.nojekyll", "must exist")


    # External links.
    if os.environ.get("SITE_CHECK_OFFLINE") != "1":
        with ThreadPoolExecutor(max_workers=8) as pool:
            for url, status in zip(external, pool.map(probe, external)):
                where = ", ".join(sorted(external[url]))
                if status in (404, 410):
                    failures.append(f"{where}: broken external link {url} ({status})")
                elif status is None or not (200 <= status < 400):
                    unverified.append(f"{where}: {url} ({status or 'no response'})")

    for line in unverified:
        print(f"UNVERIFIED {line}")
    for line in failures:
        print(f"FAIL {line}")
    print(f"check-site: {len(pages)} pages, {len(external)} external links, "
          f"{len(failures)} failures, {len(unverified)} unverified")
    return 1 if failures else 0


def probe(url: str) -> int | None:
    headers = {"User-Agent": "livespec-website-link-check"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 429, 501):
                continue
            return exc.code
        except Exception:
            if method == "HEAD":
                continue
            return None
    return None


if __name__ == "__main__":
    sys.exit(main())
