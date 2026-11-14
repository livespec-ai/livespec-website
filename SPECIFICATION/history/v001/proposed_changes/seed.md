---
topic: seed
author: livespec-seed
---

## Proposal: seed

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/contracts.md
- SPECIFICATION/constraints.md
- SPECIFICATION/non-functional-requirements.md
- SPECIFICATION/scenarios.md
- SPECIFICATION/README.md

### Summary

Initial seed of the specification from user-provided intent.

### Motivation

1. Minimal pure-html site - no javascript frameworks.
2. Published via github pages (stuff like this is in nonfunctional requirments - NFR - file of spec)
3. Domain is livespec-ai.com, with cloudflare in front of it, just like existing thewoolleyweb.com (more NFR).  
4. Minimal styling, based on existing styles from thewoolleyweb.com, under thewoolleyman/thewoolleyman with minimal 'takahashi' style - big letters, greyscale.  
5. There may need to be style additions for prose text, left justified, etc - the existing thewoolleyman styles are only for menus/centered. 
6. Initial site content is two things.  First is just a homepage with minimal info, describing me, the project goals, that it is an experimental work in progress around two goals: circular feedback loop between specification and implementation, and turning up all quality dials as close to 11 as is possible within cost/speed constraints (the fast/cheap/right-pick-two triangle).  Then a summary of the high level state of the project, relying mostly on links to existing content in livespec github repos' readmes and docs and specifications - minimal duplication of that content. 
7. Second is a blog, served under /blog, which will describe my journey towards exploring the two goals. Start with a placeholder for a single blog entry, then I will flesh out content. 
8. `just` and justfile targets should be used for any necessary scripting, but this should be minimal to none to start with, on a pure-html github pages site.
9. Site traffic metrics and seo/date will be setup (more NFR).

### Proposed Changes

1. Minimal pure-html site - no javascript frameworks.
2. Published via github pages (stuff like this is in nonfunctional requirments - NFR - file of spec)
3. Domain is livespec-ai.com, with cloudflare in front of it, just like existing thewoolleyweb.com (more NFR).  
4. Minimal styling, based on existing styles from thewoolleyweb.com, under thewoolleyman/thewoolleyman with minimal 'takahashi' style - big letters, greyscale.  
5. There may need to be style additions for prose text, left justified, etc - the existing thewoolleyman styles are only for menus/centered. 
6. Initial site content is two things.  First is just a homepage with minimal info, describing me, the project goals, that it is an experimental work in progress around two goals: circular feedback loop between specification and implementation, and turning up all quality dials as close to 11 as is possible within cost/speed constraints (the fast/cheap/right-pick-two triangle).  Then a summary of the high level state of the project, relying mostly on links to existing content in livespec github repos' readmes and docs and specifications - minimal duplication of that content. 
7. Second is a blog, served under /blog, which will describe my journey towards exploring the two goals. Start with a placeholder for a single blog entry, then I will flesh out content. 
8. `just` and justfile targets should be used for any necessary scripting, but this should be minimal to none to start with, on a pure-html github pages site.
9. Site traffic metrics and seo/date will be setup (more NFR).
