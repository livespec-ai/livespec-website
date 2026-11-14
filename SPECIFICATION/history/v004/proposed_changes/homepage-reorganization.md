---
topic: homepage-reorganization
author: claude-opus-5-5
created_at: 2026-11-14T03:31:46Z
---

## Proposal: Homepage reorganized around a dark-factory framing and a third goal

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/scenarios.md

### Summary

The homepage leads with a new "What is livespec?" section that presents livespec as a "dark" software factory and links to the author's Software Factory Practitioner's Guide on thewoolleyweb.com, then the blog link, then a "Goals" section with a third goal (finding the minimal human attention the factory needs, with its four practices as a sub-list), then the project state, and finally the author introduction under "Who is responsible for this?" using the author's professional bio.

### Motivation

Maintainer direction: reorganize the homepage into What is livespec / Blog / Goals / Where things stand / Who is responsible for this?, describe livespec as a dark software factory linking the canonical thewoolleyweb.com practitioner's guide, add a third goal about minimal human attention, and replace the author paragraph with the LinkedIn bio blurb.

### Proposed Changes

spec.md §Project intent: describe the site as explaining what livespec is, stating goals, summarizing state, introducing the author, and hosting the blog; present livespec as a "dark" software factory and experimental work in progress pursuing three goals, adding goal 3: Finding the minimal human attention the factory needs to still produce usable, high-quality implementations — interfacing only with AI surfaces, rarely if ever directly reviewing code or specification, reviewing only the delivered implementation, and relying on observability signals across every aspect of the factory and the implementation for guidance.

spec.md §Homepage: the homepage MUST contain, in this order: (1) What is livespec — livespec as a "dark" software factory and experimental work in progress, linking to https://thewoolleyweb.com/software-factory-practitioners-guide.html; (2) Blog link; (3) Goals — the three goals in order, the quality-dials goal naming the pick-two triangle, and the minimal-human-attention goal listing its four practices as a bulleted sub-list; (4) Project state (unchanged rules); (5) Author — headed "Who is responsible for this?", the author's professional bio with links to thewoolleyweb.com and github.com/thewoolleyman. §Blog: refer to "the project goals" rather than "the two project goals".

scenarios.md §Visitor reads the homepage: the visitor sees, in order, the dark-factory description with the practitioner's-guide link, the blog link, the three goals, the project-state links, and the author introduction.
