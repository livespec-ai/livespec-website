---
proposal: render-markdown-pages-to-the.md
decision: modify
revised_at: 2026-11-14T05:26:59Z
author_human: Chad Woolley <thewoolleyman@gmail.com>
author_llm: claude-opus-5-5
---

## Decision and Rationale

Maintainer approved the pandoc plan in-session (2026-11-13, work item lsw-gg7lzm) with rulings: every HTML page under site/ is converted to Markdown; local review uses file:// URLs with no HTTP server (just serve removed; just preview prints and opens the file:// URL); the render-drift check ignores whitespace-only differences; a zero-dependency polling just watch re-renders on change. The independent review's one blocker (404.html must stay root-absolute) was fixed before the final NO BLOCKERS verdict.

## Modifications

1. Added `just watch` (zero-dependency polling re-render, about once per second) with a scenario bounded at 3 seconds that also covers template changes (maintainer ruling). 2. The render bullet describes the pandoc reader as GitHub-flavored Markdown with YAML front matter and explicit heading attributes and without automatic heading identifiers (pandoc's gfm reader adds heading ids by default, which would change existing markup), instead of naming exact flags. 3. Template links are computed per page: the shortest relative path on every page, root-absolute on /404.html (review blocker: contracts.md requires root-absolute links on 404.html). 4. Dropped the restatement that rendered pages satisfy contracts.md (Definition of Done already requires it); the spec.md non-goal says rendering runs before commit rather than at deploy time, and the MUST NOT stays in non-functional-requirements.md §Publishing. 5. Tooling wording: helper scripts under scripts/ are invoked only through just recipes, and scripts/ is added to the layout table.

## Resulting Changes

- spec.md
- constraints.md
- non-functional-requirements.md

## Ratification Review

ratification_review: manual-spawn
reviewer_model: claude-opus-5-5
reviewer_identity: claude-opus-5-5
separate_reviewer: True
read_only: True
reviewed_at: 2026-11-14T05:26:24Z
verdict: NO BLOCKERS
proposal_stem: render-markdown-pages-to-the
content_digest: bbc9cafec2dd2f60bbe25fe52bd55cca51103375cd2c05b9f53d78c739b97029
