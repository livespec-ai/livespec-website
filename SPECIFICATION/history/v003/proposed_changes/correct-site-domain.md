---
topic: correct-site-domain
author: claude-opus-5-5
created_at: 2026-11-14T00:32:57Z
---

## Proposal: correct-site-domain-to-livespec-ai-org

### Target specification files

- SPECIFICATION/README.md
- SPECIFICATION/spec.md
- SPECIFICATION/contracts.md
- SPECIFICATION/constraints.md
- SPECIFICATION/non-functional-requirements.md
- SPECIFICATION/scenarios.md

### Summary

The specification names the site's domain as livespec-ai.com throughout (title, canonical origin, URL surface, hosting, Cloudflare, GoatCounter, Search Console, sitemap, scenarios). The correct domain is livespec-ai.org.

### Motivation

Maintainer correction: the site's domain is livespec-ai.org, not livespec-ai.com. Every requirement keyed to the domain is currently wrong.

### Proposed Changes

Replace every occurrence of `livespec-ai.com` with `livespec-ai.org` in all six live spec files, including the H1 titles, `https://livespec-ai.com` origins and URLs, `www.livespec-ai.com`, the `site/CNAME` content, and the Cloudflare zone name. No other text changes.
