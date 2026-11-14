---
topic: render-markdown-pages-to-the
author: claude-opus-5-5
created_at: 2026-11-14T05:21:16Z
---

## Proposal: Pages are authored in Markdown and rendered to committed static HTML with pandoc

### Target specification files

- SPECIFICATION/spec.md

### Summary

Replace the 'hand-authored static HTML, no build step' architecture and the blanket static-site-generator non-goal with: every page is authored as Markdown and rendered to static HTML by pandoc with one shared page template; the rendered HTML is committed under site/ and is what visitors receive, so the deploy still uploads site/ as committed.

### Motivation

Work item lsw-gg7lzm: adopt pandoc as a minimal Markdown-to-HTML renderer (mirroring thewoolleyman/software-factory-practitioners-guide) so blog entries and pages can be written in Markdown. The ratified text forbids it in spec.md Architecture ('hand-authored static HTML pages ... There is no build step') and Non-goals ('No ... static-site generator'). Visitors still receive plain static HTML and CSS; only the authoring source changes.

### Proposed Changes

In spec.md §Architecture, replace the first paragraph with:

> The site is a set of static HTML pages plus one shared stylesheet, served by GitHub Pages behind Cloudflare. Each page is authored as Markdown and rendered to HTML with pandoc through one shared page template; the rendered HTML is committed under `site/` and is what visitors receive. There is no deploy-time build step, no client-side framework, and no server-side code.

The Architecture diagram is unchanged.

In spec.md §Non-goals, replace the first bullet with:

> - No JavaScript framework, bundler, or transpiler, and no static-site generator beyond pandoc rendering each Markdown page through the one shared page template. Rendering MUST NOT run at deploy time.

The Per-page HTML contract, Blog entry contract, and URL surface in contracts.md apply unchanged to rendered pages: a rendered page MUST satisfy them exactly as a hand-authored page did.

## Proposal: Markdown elements inside prose are styled in the greyscale palette

### Target specification files

- SPECIFICATION/constraints.md

### Summary

Add a Styling constraint that the GitHub-flavored Markdown elements pandoc can emit inside prose (tables, code blocks, inline code, blockquotes) are styled by the one stylesheet in the greyscale palette at WCAG 2.2 AA contrast.

### Motivation

Markdown authoring makes tables, code, and blockquotes easy to write; takahashi default.css does not style them consistently with the prose style. Their appearance is visitor-observable, so the rule belongs in constraints.md §Styling.

### Proposed Changes

In constraints.md §Styling, append the bullet:

> - Tables, code blocks, inline code, and blockquotes inside prose MUST be styled by `/css/style.css` in the greyscale palette, with text meeting WCAG 2.2 AA contrast, and MUST NOT cause horizontal page scrolling at 360 px width (wide tables and code blocks scroll within their own box).

## Proposal: Contributor rendering toolchain, preview, render-drift check, and layout

### Target specification files

- SPECIFICATION/non-functional-requirements.md

### Summary

Add pandoc to the contributor toolchain, define just render and just preview, add a whitespace-insensitive render-drift check to just check, place Markdown sources in content/ and the page template in templates/ (both unpublished), and keep the deploy a plain upload of the committed site/ directory; add scenarios for render drift and preview.

### Motivation

Work item lsw-gg7lzm and maintainer rulings 2026-11-13: every HTML page under site/ is converted to Markdown; local review opens the rendered file:// URL directly with no HTTP server (just serve is removed); just check gates that committed HTML matches what the Markdown renders to, ignoring whitespace-only differences. non-functional-requirements.md currently says 'Pages are hand-authored HTML', lists only uv/just/lefthook, and has no render step or drift check.

### Proposed Changes

In non-functional-requirements.md §Spec → Development discipline, replace the 'Pages are hand-authored HTML' bullet with:

> - Every HTML page under `site/` is rendered from a Markdown source under `content/`; contributors edit the Markdown source, never the rendered HTML directly. Edits preserve the site's existing markup conventions, relative structure, and published URLs. Site-specific markup MAY be written as raw HTML inside the Markdown.

In §Tooling and enforcement, replace the first bullet's last sentence with: "Scripting is kept minimal — the site itself needs none to be served; rendering runs only on contributor machines and in the check job."

In §Contracts → Contributor toolchain, replace the first sentence with: "Tools are pinned in `.mise.toml` and run via `mise exec --`: `uv` (Python, for livespec dev-tooling and site checks), `just`, `lefthook`, and `pandoc` (Markdown rendering). `just bootstrap` MUST install every pinned tool." Then add:

> ### Render and preview commands
>
> - `just render` MUST render every `content/**/*.md` source to its page under `site/` with `pandoc --from=gfm+yaml_metadata_block --to=html5` and the one shared template in `templates/`. Per-page metadata (title, description, canonical path, Open Graph type, dates, GoatCounter path) comes from the source's YAML front matter. The relative path from a page to the site root MUST be supplied to the template so every internal link and the stylesheet link stays relative, per contracts.md §URL surface.
> - `just preview` MUST run `just render`, print the `file://` URL of `site/index.html`, and open it with the platform opener (`open` on macOS, `xdg-open` on Linux). No HTTP server is part of the contributor toolchain.

In §Check-aggregate command, add item 4:

> 4. **Render-drift check** — every Markdown source under `content/` is rendered to a temporary location and compared with its committed page under `site/`, ignoring whitespace-only differences; any other difference, a Markdown source without a committed page, or an HTML page under `site/` without a Markdown source MUST fail and name the page.

In §Publishing, replace the second bullet with:

> - A GitHub Actions workflow deploys `site/` to GitHub Pages on every push to `main` (Pages source: GitHub Actions). The deploy uploads the committed `site/` directory as-is and MUST NOT render pages. The workflow's check job installs the pinned toolchain (including pandoc) through mise and runs `just check`, including the render-drift check, before the deploy job runs.

In §Constraints → Repository layout, add rows:

> | `content/` | Markdown sources, one per HTML page under `site/` (never published) |
> | `templates/page.html` | The one shared pandoc page template (never published) |

and add `scripts/` to the Contributor tooling row.

In §Scenarios, add:

> ### Scenario: An edited page that was not re-rendered blocks the change
>
> Given a Markdown source under `content/` has been edited
>
> And its committed page under `site/` was not re-rendered
>
> When a contributor runs `just check`
>
> Then the check fails and names the page whose rendered HTML differs from its committed HTML
>
> ### Scenario: Whitespace-only differences do not block the change
>
> Given a committed page under `site/` differs from its rendered Markdown source only in whitespace
>
> When a contributor runs `just check`
>
> Then the render-drift check passes for that page
>
> ### Scenario: A contributor previews the rendered site locally
>
> Given a contributor has edited a Markdown source under `content/`
>
> When the contributor runs `just preview`
>
> Then every page is re-rendered under `site/`
>
> And the `file://` URL of `site/index.html` is printed and opened in the platform's default browser without starting an HTTP server
