---
proposal: relative-stylesheet.md
decision: accept
revised_at: 2026-11-14T03:47:51Z
author_human: Chad Woolley <thewoolleyman@gmail.com>
author_llm: claude-opus-5-5
---

## Decision and Rationale

Maintainer directed this in-session: the stylesheet and all internal links must be relative so the site renders and navigates from file:// for local review. The independent review's blocker (literal '/' and '/blog/' link targets) is resolved by the link-target sentence in the URL-surface rule.

## Resulting Changes

- contracts.md
- scenarios.md

## Ratification Review

ratification_review: manual-spawn
reviewer_model: claude-opus-5-5
reviewer_identity: claude-opus-5-5
separate_reviewer: True
read_only: True
reviewed_at: 2026-11-14T03:47:34Z
verdict: NO BLOCKERS
proposal_stem: relative-stylesheet
content_digest: d0a3767c40545d6d40b1137001a4020d0e45a49f4b667a36eaa42e7756be0ce7
