---
proposal: maintainer-direct-content-edits.md
decision: accept
revised_at: 2026-11-14T19:01:54Z
author_human: Chad Woolley <thewoolleyman@gmail.com>
author_llm: claude-opus-5-5
---

## Decision and Rationale

Maintainer requested and approved this design in-session (2026-11-14, work item lsw-8tk): Markdown sources edited directly on main, e.g. in the GitHub web editor, must go live with no local tooling. Rendering moves to deploy time, rendered HTML becomes gitignored build output, the render-drift check is retired, and the maintainer (only) may commit directly to main while agents keep the worktree-and-PR rule. This deliberately reverses v006's 'rendered before commit, no deploy-time build' choice at the maintainer's direction. Scope is this repository's specification only.

## Resulting Changes

- spec.md
- non-functional-requirements.md
- scenarios.md

## Ratification Review

ratification_review: manual-spawn
reviewer_model: claude-opus-5-5
reviewer_identity: claude-opus-5-5
separate_reviewer: True
read_only: True
reviewed_at: 2026-11-14T19:00:30Z
verdict: NO BLOCKERS
proposal_stem: maintainer-direct-content-edits
content_digest: c7cb6ac7e5cb28955788a332e4aa00fe088fe528ad93349d2e9cdb4645d24ada
