---
topic: relative-stylesheet
author: claude-opus-5-5
created_at: 2026-11-14T03:13:00Z
---

## Proposal: Relative internal links and stylesheet for file:// review

### Target specification files

- SPECIFICATION/contracts.md
- SPECIFICATION/scenarios.md

### Summary

Internal links and the stylesheet link become relative paths that name the target file (`blog/index.html`, `../css/style.css`), so a maintainer can open `site/*.html` straight from the filesystem and both see it styled and navigate between pages without a local server. Canonical URLs keep the trailing-slash form. `/404.html` keeps root-absolute paths because GitHub Pages serves it at arbitrary request paths.

### Motivation

Maintainer feedback: opening file:///.../site/index.html renders without CSS and the blog link is broken locally; the CSS and all links should be relative so local review works without a test server.

### Proposed Changes

contracts.md §URL surface rules: replace the bullet "Directory URLs are served from `<dir>/index.html`; links MUST use the trailing-slash directory form (`/blog/`, not `/blog/index.html`)." with two bullets: (1) Directory URLs are served from `<dir>/index.html`. Canonical URLs (canonical tags, Open Graph URLs, the sitemap) MUST use the trailing-slash directory form (`/blog/`, not `/blog/index.html`). (2) Internal links and the stylesheet link MUST be relative paths that name the target file (`blog/index.html`, `../css/style.css`), so the site navigates and renders when opened from the filesystem for local review. `/404.html` MUST instead use root-absolute paths, because GitHub Pages serves it at arbitrary request paths. Wherever this specification names an internal link target by its URL (e.g. `/`, `/blog/`), it identifies the target page; the `href` form is governed by this rule.

contracts.md §Per-page HTML contract: replace "Link the stylesheet as `/css/style.css` and no other stylesheet." with "Link exactly one stylesheet, `/css/style.css`, by the path form the URL-surface rules above require."

scenarios.md: add, before "Search engine indexes the site", a scenario "Maintainer reviews the site from the filesystem": Given a maintainer opens `site/index.html` from a local checkout via a `file://` URL / When the page loads and the maintainer follows the header, body, and footer links / Then every page renders with the site stylesheet / And every internal link opens the target page rather than a directory listing.
