---
topic: remove-content-overspecification
author: claude-opus-5-5
created_at: 2026-11-14T04:57:48Z
---

## Proposal: Stop specifying homepage and placeholder content

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/scenarios.md

### Summary

The spec over-specified editorial content: the homepage section order, headings, per-section length limits, the exact practices listed under goal 3, a practitioner's-guide link, and the placeholder entries' titles, dates, summaries, and body style. Adding or rewording content invalidated the spec. The homepage requirement becomes a set of required content areas (what livespec is, blog link, goals, repository links with the three minimum targets, author introduction with two links) with wording, order, headings, and additional content left to the author; goal 3 is stated without its practice list; placeholder entries need only be clearly marked.

### Motivation

Maintainer ruling: the author's homepage edits are just content. If anything in the specification is invalidated by adding content, it is overspecified and should be removed.

### Proposed Changes

spec.md §Project intent: goal 3 becomes "Finding the minimal human attention the factory needs to still produce usable, high-quality implementations." (drop the practice list).

spec.md §Homepage: replace the ordered five-item list with: The homepage MUST contain: a description of what livespec is; a link to `/blog/`; the project goals named in Project intent; links to the livespec GitHub repositories, including at minimum the core `thewoolleyman/livespec` repository's README, its installation documentation, and its `SPECIFICATION/` tree; an introduction to the author, Chad Woolley ("thewoolleyman"), with links to `https://thewoolleyweb.com/` and `https://github.com/thewoolleyman`. The wording, order, headings, and any additional content are the author's editorial choice.

spec.md §Blog: replace the two-placeholder-entries bullet with: Until the author writes real entries, the blog MAY contain placeholder entries; each placeholder MUST be clearly marked as a placeholder. Entry titles, dates, and body content are the author's editorial choice.

scenarios.md §Visitor reads the homepage: replace the ordered first/next/finally steps with unordered steps: the visitor sees a description of what livespec is; a link to the blog; the project goals; links to the livespec GitHub repositories including the core README, installation documentation, and specification; and an introduction to Chad Woolley ("thewoolleyman").

scenarios.md §Visitor browses the blog: "When the visitor selects a placeholder entry" becomes "When the visitor selects an entry"; the arrival step shows the entry's title, author, publication date, and body (not "placeholder text"); add "And if the entry is a placeholder, it is clearly marked as a placeholder". Rename the scenario "Visitor follows a project-state link" to "Visitor follows a repository link" (the homepage no longer has a required project-state section).
