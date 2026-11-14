---
topic: maintainer-direct-content-edits
author: claude-opus-5-5
created_at: 2026-11-14T18:59:26Z
---

## Proposal: Render pages at deploy time instead of committing rendered HTML

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/non-functional-requirements.md
- SPECIFICATION/scenarios.md

### Summary

Rendered HTML pages under site/ stop being committed: they become a gitignored build output that `just render` produces locally and that the GitHub Actions deploy job produces from the pushed commit's Markdown sources before uploading site/. `just check` renders first so it checks exactly what will deploy, and the render-drift check (with its two scenarios) is removed because nothing rendered is committed to drift.

### Motivation

The maintainer wants to edit a Markdown source under content/ directly on main (for example in the GitHub web editor) and have the live site update automatically, with no local tooling. Today the rendered HTML is committed and CI's render-drift check fails any commit that changes a source without re-rendering, so such an edit blocks the deploy and never goes live. Rendering in CI removes the need for a local pandoc run.

### Proposed Changes

spec.md §"Architecture": replace "the rendered HTML is committed under `site/` and is what visitors receive. There is no deploy-time build step, no client-side framework, and no server-side code." with "the deploy workflow renders the pages from the Markdown sources on every push to `main`, and the rendered HTML under `site/` is what visitors receive; it is a build output and MUST NOT be committed. There is no client-side framework and no server-side code." In the diagram, the repo node becomes `livespec-ai/livespec-website<br/>content/ + site/ assets` with edge label `render + deploy on push to main`.

spec.md §"Non-goals": replace ", run before commit rather than at deploy time." with ", run by the deploy workflow and on contributor machines for local preview."

non-functional-requirements.md §"Development discipline", third bullet: append "Rendered HTML pages under `site/` are build output: they MUST be gitignored and MUST NOT be committed. Static assets under `site/` (`css/`, `CNAME`, `robots.txt`, `sitemap.xml`, `.nojekyll`) stay committed."

non-functional-requirements.md §"Tooling and enforcement": replace "rendering runs only on contributor machines and in the check job." with "rendering runs only on contributor machines and in the GitHub Actions workflow."

non-functional-requirements.md §"Render, preview, and watch commands", first bullet: append "Before rendering, `just render` MUST remove every previously rendered HTML page under `site/`, so a deleted or renamed source leaves no stale page."

non-functional-requirements.md §"Check-aggregate command": the intro becomes "`just check` MUST first run `just render`, so it checks exactly the pages a deploy of the same commit would publish, then runs, at minimum:" and item 4 (Render-drift check) is removed.

non-functional-requirements.md §"Publishing", second bullet becomes: "A GitHub Actions workflow deploys `site/` to GitHub Pages on every push to `main` (Pages source: GitHub Actions). The workflow's check job installs the pinned toolchain (including pandoc) through mise and runs `just check`; a failing check MUST block the deploy job. The deploy job MUST install the same pinned toolchain through mise and run `just render` on the pushed commit before uploading `site/`."

non-functional-requirements.md §"Repository layout": the `site/` row becomes "Everything published: rendered HTML (build output, gitignored), and committed `css/`, `robots.txt`, `sitemap.xml`, `CNAME`, `.nojekyll`"; the `site/blog/<slug>/index.html` row becomes "One rendered blog entry (from `content/blog/<slug>/index.md`)"; the `content/` row becomes "Markdown sources, one per rendered HTML page under `site/` (never published)".

non-functional-requirements.md §"Scenarios": in "A merged change is published and verified live", the Given becomes "Given a pull request that changes a Markdown source under `content/` or a file under `site/`". The scenarios "An edited page that was not re-rendered blocks the change" and "Whitespace-only differences do not block the change" are removed. Add:

### Scenario: Checking renders the pages first

Given a Markdown source under `content/` has been edited and `just render` has not been run

When a contributor runs `just check`

Then the pages are rendered from the edited source before any check runs

And the checks report on the newly rendered pages

### Scenario: A deleted source leaves no stale page

Given a Markdown source under `content/` was rendered and then deleted

When a contributor runs `just render`

Then no HTML page for the deleted source remains under `site/`

scenarios.md "Maintainer reviews the site from the filesystem": the Given becomes "Given a maintainer has run `just render` in a local checkout and opens `site/index.html` via a `file://` URL".

## Proposal: Maintainer may commit content edits directly to main

### Target specification files

- SPECIFICATION/non-functional-requirements.md

### Summary

Adds a maintainer-only exception to the worktree-and-pull-request rule: the maintainer MAY commit directly to `main`, for example by editing a Markdown source in the GitHub web editor, and that commit deploys like any other push. Agents MUST NOT use the exception. Adds scenarios for a direct edit going live and for a direct edit that fails a check being blocked.

### Motivation

The maintainer wants quick content fixes to go live from the GitHub web UI with no branch, worktree or pull request. The worktree discipline exists to govern agent work and stays in force for agents; the exception scopes to the maintainer acting directly, and lives only in this repository's specification so no other livespec repository's rules change.

### Proposed Changes

non-functional-requirements.md §"Development discipline": replace the first bullet with: "Every change an agent makes to a tracked file is made in an isolated git worktree (`just worktree-create <branch>`) and lands through a pull request against `main`; the primary checkout is never edited directly. Maintainer exception: the maintainer MAY commit directly to `main` (for example by editing a file in the GitHub web editor), and such a commit is checked and deployed like any other push to `main`. Agents MUST NOT commit or push directly to `main`, even when acting on the maintainer's behalf."

non-functional-requirements.md §"Scenarios": add

### Scenario: The maintainer's direct content edit goes live

Given the maintainer edits a Markdown source under `content/` in the GitHub web editor

And commits the edit directly to `main`

When the GitHub Actions workflow runs for that commit

Then the check job renders and checks the pages and passes

And the deploy job renders the pages and publishes them

And fetching the edited page on `https://livespec-ai.org/` returns the new content

### Scenario: A direct edit that fails a check is not published

Given the maintainer commits directly to `main` a Markdown source edit that breaks an internal link

When the GitHub Actions workflow runs for that commit

Then the check job fails and names the referring page and the broken URL

And the deploy job does not run, so the live site is unchanged
