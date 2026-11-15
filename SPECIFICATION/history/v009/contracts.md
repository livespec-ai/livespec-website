# livespec-ai.org — contracts

This file enumerates the site's externally observable interfaces:
its URL surface and the per-page HTML contract every page honors.

## URL surface

All URLs are served from the canonical origin
`https://livespec-ai.org`.

| URL | Content |
|---|---|
| `/` | Homepage |
| `/blog/` | Blog index |
| `/blog/<slug>/` | One blog entry |
| `/css/style.css` | The single site stylesheet |
| `/robots.txt` | Crawler directives; references the sitemap |
| `/sitemap.xml` | XML sitemap listing every HTML page |
| `/404.html` | Not-found page (served by GitHub Pages for unknown paths) |

Rules:

- `http://` requests MUST redirect to `https://`.
- `https://www.livespec-ai.org/<path>` MUST redirect permanently
  to `https://livespec-ai.org/<path>`.
- Directory URLs are served from `<dir>/index.html`. Canonical
  URLs (canonical tags, Open Graph URLs, the sitemap) MUST use the
  trailing-slash directory form (`/blog/`, not
  `/blog/index.html`).
- Internal links and the stylesheet link MUST be relative paths
  that name the target file (`blog/index.html`,
  `../css/style.css`), so the site navigates and renders when
  opened from the filesystem for local review. `/404.html` MUST
  instead use root-absolute paths, because GitHub Pages serves it
  at arbitrary request paths. Wherever this specification names an
  internal link target by its URL (e.g. `/`, `/blog/`), it
  identifies the target page; the `href` form is governed by this
  rule.
- A published URL MUST NOT be removed or renamed without a
  redirect page at the old URL.

## Per-page HTML contract

Every HTML page MUST:

- Be a valid HTML5 document starting with `<!DOCTYPE html>`, with
  `<html lang="en">` and `<meta charset="utf-8">`.
- Include `<meta name="viewport" content="width=device-width,
  initial-scale=1">`.
- Have a unique `<title>` and a unique
  `<meta name="description">` describing that page.
- Include `<link rel="canonical">` with the page's absolute
  canonical URL on `https://livespec-ai.org`.
- Include Open Graph tags `og:title`, `og:description`, `og:url`,
  and `og:type` (`website` for the homepage and blog index,
  `article` for blog entries).
- Link exactly one stylesheet, `/css/style.css`, by the path form
  the URL-surface rules above require.
- Include the site traffic-metrics tag (see
  [constraints.md](constraints.md#traffic-metrics)).
- Contain a header with the site title linking to `/`, and a
  footer linking to `/`, `/blog/`, the `livespec-ai/livespec`
  GitHub repository, and `https://thewoolleyweb.com/`.

## Blog entry contract

Each blog entry page additionally MUST:

- Wrap the entry in an `<article>` element whose `<header>`
  contains the entry's `<h1>` title and a byline naming the author
  and the publication `<time datetime="YYYY-MM-DD">`.
- Include `<meta name="author" content="Chad Woolley">` and
  `<meta property="article:author" content="https://thewoolleyweb.com/">`.
- Mark its publication date with
  `<time datetime="YYYY-MM-DD">` and include
  `<meta property="article:published_time" content="YYYY-MM-DD">`.
- Include, when it has been revised after publication, a
  `<time datetime="YYYY-MM-DD">` "updated" date and
  `<meta property="article:modified_time">`.
- Appear in the `/blog/` index and in `/sitemap.xml`.

## Sitemap contract

`/sitemap.xml` MUST follow the sitemaps.org 0.9 protocol, list
every published HTML page except `/404.html` by absolute canonical
URL, and give each a `<lastmod>` date equal to that page's most
recent content change.
