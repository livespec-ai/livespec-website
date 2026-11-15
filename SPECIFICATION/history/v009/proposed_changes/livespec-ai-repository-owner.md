---
topic: livespec-ai-repository-owner
author: claude-fable-5-1
created_at: 2026-11-15T17:42:46Z
---

## Proposal: Name the livespec repositories by their livespec-ai owner

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/contracts.md
- SPECIFICATION/scenarios.md
- SPECIFICATION/non-functional-requirements.md

### Summary

The livespec fleet repositories moved from github.com/thewoolleyman/<repo> to github.com/livespec-ai/<repo> on 2026-11-15, and the site's rendered sources were updated to the new owner (livespec-website PR #22, live as of Pages run 43742211642). Four spec passages still name the old owner and now disagree with the site: the homepage content clause in spec.md names the core repository as `thewoolleyman/livespec`; the page contract in contracts.md requires the footer to link to the `thewoolleyman/livespec` GitHub repository; the installation-link scenario in scenarios.md says the visitor arrives in the `thewoolleyman/livespec` GitHub repository; and the render scenario in non-functional-requirements.md uses `https://github.com/thewoolleyman/livespec/blob/main/README.md` as its example external link. Each is restated with the `livespec-ai` owner, path and wording otherwise unchanged. The author's personal profile link `https://github.com/thewoolleyman` in spec.md is a user profile, not a moved repository, and is deliberately left as it is.

### Motivation

Maintainer direction (2026-11-15) to point every livespec repository link at the new livespec-ai organization and deploy; the coordinator's follow-up that the specification must not keep naming the footer target and the core repository by an owner the site no longer links to. Re-stating the owner keeps the spec the source of truth for what the rendered pages and `scripts/check-site.py`'s footer-link expectation already carry.

### Proposed Changes

Each of the four passages MUST name the core livespec repository under the `livespec-ai` owner. The footer contract MUST require a link to the `livespec-ai/livespec` GitHub repository; the homepage content clause MUST name the core `livespec-ai/livespec` repository; the installation-link scenario MUST say the visitor arrives in the `livespec-ai/livespec` GitHub repository; the render scenario's example external link MUST be `https://github.com/livespec-ai/livespec/blob/main/README.md`. The author's personal profile link `https://github.com/thewoolleyman` MUST NOT change: it names a user, not a repository, and did not move.

```diff
--- a/SPECIFICATION/spec.md
+++ b/SPECIFICATION/spec.md
@@
 - links to the livespec GitHub repositories, including at minimum
-  the core `thewoolleyman/livespec` repository's README, its
+  the core `livespec-ai/livespec` repository's README, its
   installation documentation, and its `SPECIFICATION/` tree;
--- a/SPECIFICATION/contracts.md
+++ b/SPECIFICATION/contracts.md
@@
 - Contain a header with the site title linking to `/`, and a
-  footer linking to `/`, `/blog/`, the `thewoolleyman/livespec`
+  footer linking to `/`, `/blog/`, the `livespec-ai/livespec`
   GitHub repository, and `https://thewoolleyweb.com/`.
--- a/SPECIFICATION/scenarios.md
+++ b/SPECIFICATION/scenarios.md
@@
-Then the visitor arrives at that documentation in the `thewoolleyman/livespec` GitHub repository
+Then the visitor arrives at that documentation in the `livespec-ai/livespec` GitHub repository
--- a/SPECIFICATION/non-functional-requirements.md
+++ b/SPECIFICATION/non-functional-requirements.md
@@
-And it links to `https://github.com/thewoolleyman/livespec/blob/main/README.md`
+And it links to `https://github.com/livespec-ai/livespec/blob/main/README.md`
```
