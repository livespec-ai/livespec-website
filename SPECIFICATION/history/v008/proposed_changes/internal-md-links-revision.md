---
proposal: internal-md-links.md
decision: accept
revised_at: 2026-11-14T20:04:33Z
author_human: Chad Woolley <thewoolleyman@gmail.com>
author_llm: claude-opus-5-5
---

## Decision and Rationale

Maintainer request (2026-11-14, in-session): since v007 rendered HTML is not committed, so source links to .html pages are broken when browsing content/ in the GitHub web UI. Sources link to .md sources and just render rewrites relative .md links to .html, leaving scheme, protocol-relative and root-absolute links unchanged.

## Resulting Changes

- non-functional-requirements.md

## Ratification Review

ratification_review: manual-spawn
reviewer_model: claude-opus-5-5
reviewer_identity: claude-opus-5-5
separate_reviewer: True
read_only: True
reviewed_at: 2026-11-14T20:04:30Z
verdict: NO BLOCKERS
proposal_stem: internal-md-links
content_digest: 93e86b8c41adc07ac69a315ff14ba61ea28856b105c3f0929f7057d3bfebed04
