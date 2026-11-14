---
topic: claude-opus-5-5-critique
author: claude-opus-5-5
created_at: 2026-11-14T00:29:32Z
---

## Proposal: dod-pre-and-post-merge-split

### Target specification files

- SPECIFICATION/spec.md

### Summary

spec.md §"Definition of Done" opens with "A livespec-website change MUST satisfy this DoD before merge", but its last item ("After merge, the change is verified live on https://livespec-ai.com/") can only be satisfied after merge.

### Motivation

The DoD is internally contradictory: one of its required items cannot hold at the moment the DoD says all items must hold, leaving it unclear whether live verification gates merge or follows it.

### Proposed Changes

Split spec.md §"Definition of Done" into two lists. "Before merge": the change MUST flow through the propose-change/revise loop with no out-of-band edits; every page MUST conform to contracts.md and constraints.md; the site-wide link check MUST pass; the doctor static phase MUST pass. "After merge": the change MUST be verified live on https://livespec-ai.com/ per non-functional-requirements.md §"Contributor workflow"; a change is not done until that verification succeeds.

## Proposal: single-home-for-greyscale-and-www-redirect

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/contracts.md
- SPECIFICATION/constraints.md

### Summary

The greyscale-palette rule is stated normatively in both spec.md §"Visual style" ("The palette MUST be greyscale only") and constraints.md §"Styling". The www-to-apex redirect is stated in both contracts.md §"URL surface" (MUST redirect permanently) and constraints.md §"Hosting and domain".

### Motivation

Duplicated normative rules invite inconsistency: when one copy is revised and the other is not, the spec becomes contradictory, and the two existing copies already differ in strength (the constraints.md redirect bullet is silent on permanence).

### Proposed Changes

Keep each rule in exactly one file. Greyscale: constraints.md §"Styling" remains the normative home; in spec.md §"Visual style" remove the bullet "The palette MUST be greyscale only (no hue)." and the trailing "and still greyscale" phrase, replacing them with a cross-reference to [constraints.md](constraints.md#styling). Redirect: contracts.md §"URL surface" remains the normative home (permanent redirect); in constraints.md §"Hosting and domain" replace the bullet "`www.livespec-ai.com` redirects to the apex." with a cross-reference to [contracts.md](contracts.md#url-surface).
