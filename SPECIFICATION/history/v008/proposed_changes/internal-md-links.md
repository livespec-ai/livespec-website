---
topic: internal-md-links
author: claude-opus-5-5
created_at: 2026-11-14T20:03:15Z
---

## Proposal: Markdown sources link to each other by their .md paths

### Target specification files

- SPECIFICATION/non-functional-requirements.md

### Summary

Internal links in Markdown sources target the linked page's Markdown source by relative path (e.g. `blog/index.md`), so they work when browsing `content/` on GitHub, and `just render` rewrites every relative link whose path ends in `.md` to the corresponding `.html` page, in both Markdown links and raw HTML `href` attributes. Links with a URL scheme, protocol-relative links, and root-absolute links are left unchanged.

### Motivation

Since v007 the rendered HTML is not committed, so a source link such as `blog/index.html` is broken when the maintainer navigates the Markdown sources in the GitHub web UI. Linking to the `.md` source fixes navigation on GitHub while the rendered site keeps its `.html` URLs.

### Proposed Changes

non-functional-requirements.md §"Development discipline", third bullet: after "Site-specific markup MAY be written as raw HTML inside the Markdown." add "An internal link in a Markdown source SHOULD target the linked page's Markdown source by relative path (for example `blog/index.md`), so the link also works when browsing `content/` on GitHub."

non-functional-requirements.md §"Render, preview, and watch commands": add a bullet after the `just render` bullet: "`just render` MUST rewrite every relative link whose path ends in `.md` (optionally followed by a `?query` or `#fragment`, which are kept) to the same path ending in `.html`, both in Markdown links and in `href` attributes of raw HTML in the source. It MUST NOT rewrite a link that has a URL scheme (such as `https:` or `mailto:`), a protocol-relative link (`//host/...`), or a root-absolute link (`/...`)."

non-functional-requirements.md §"Scenarios": add

### Scenario: Internal .md links render as .html links

Given a Markdown source under `content/` links to `blog/index.md` in a Markdown link and to `the-journey-begins/index.md#intro` in a raw HTML `href`

And it links to `https://github.com/thewoolleyman/livespec/blob/main/README.md`

When a contributor runs `just render`

Then the rendered page links to `blog/index.html` and `the-journey-begins/index.html#intro`

And the external link to `README.md` on GitHub is unchanged
