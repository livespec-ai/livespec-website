# livespec-ai.org — constraints

Architecture-level constraints whose violation a visitor could
observe.

## Runtime

- The site is pure static HTML and CSS served by GitHub Pages.
- Pages MUST render fully, with all content readable and all
  navigation working, with JavaScript disabled.
- No JavaScript framework, library, or bundle is permitted. The
  only permitted JavaScript is the third-party traffic-metrics tag
  (see [Traffic metrics](#traffic-metrics)) and any script
  Cloudflare injects at the edge.
- Pages MUST render correctly in current evergreen browsers at
  phone width (360 px) and desktop width without horizontal
  scrolling. The inherited takahashi `min-width: 770px` rule MUST
  NOT be carried over.

## Hosting and domain

- The site is served at the apex domain `livespec-ai.org` over
  HTTPS only.
- Cloudflare proxies the domain in front of GitHub Pages, matching
  the existing `thewoolleyweb.com` arrangement.
- The `www` and `http` redirect behavior is specified in
  [contracts.md](contracts.md#url-surface).

## Styling

- One stylesheet, `/css/style.css`, derived from takahashi
  `default.css` and extended with a prose style.
- Greyscale palette only; no colored hue anywhere on the site.
- Font stack inherited from takahashi (`Verdana, Tahoma, Arial,
  sans-serif`); no web-font downloads.
- Prose and article blocks MUST be start-aligned (never fully
  justified), normal weight, with a line height of about 1.6 to
  1.75 and a maximum line length of about 70 characters.
- The blog article header MUST place title, byline, and body in
  the same column; the byline MUST use a smaller size and a muted
  grey that still meets WCAG 2.2 AA contrast.
- Tables, code blocks, inline code, and blockquotes inside prose
  MUST be styled by `/css/style.css` in the greyscale palette, with
  text meeting WCAG 2.2 AA contrast, and MUST NOT cause horizontal
  page scrolling at 360 px width (wide tables and code blocks
  scroll within their own box).
- Text and background colors MUST meet WCAG 2.2 AA contrast.

## Traffic metrics

- Every HTML page MUST carry the site's traffic-metrics tag so
  page views are recorded.
- The provider is GoatCounter (`goatcounter.com`), using the
  site code dedicated to `livespec-ai.org`.
- The tag is GoatCounter's `count.js` script, loaded with `async`
  so it MUST NOT block rendering, plus a `<noscript>` GoatCounter
  pixel image so visits with JavaScript disabled are still counted.
- Traffic metrics MUST NOT set cookies.

## Search engine optimization

- Every page carries the SEO metadata in
  [contracts.md](contracts.md#per-page-html-contract).
- `/robots.txt` allows all crawlers and references
  `https://livespec-ai.org/sitemap.xml`.
- The domain is verified in Google Search Console and the sitemap
  is submitted there.

## Dependencies

- No package-manager dependencies are shipped to visitors.
- External resources loaded by pages are limited to the
  GoatCounter script and pixel.
