# livespec-ai.org — non-functional requirements

This document MUST be read alongside `spec.md`, `contracts.md`,
`constraints.md`, and `scenarios.md`. It enumerates how the site is
built, checked, published, and maintained — concerns not visible to
a site visitor.

## Boundary

`non-functional-requirements.md` covers "how the project is built,
tested, published, and maintained". The sections below mirror the
user-facing spec files:

- `## Spec` — process intent and behavior: development discipline,
  what "done" means for a contributor change.
- `## Contracts` — contributor-facing toolchain and commands.
- `## Constraints` — repository layout, publishing, and
  infrastructure invariants that bind contributors.
- `## Scenarios` — contributor-facing Gherkin scenarios.

The boundary against the user-facing files: anything a visitor
could observe (URLs, page content, HTML metadata, styling, HTTPS
and redirect behavior) stays in `spec.md`, `contracts.md`,
`constraints.md`, or `scenarios.md`. Hosting, DNS, deployment
mechanics, GoatCounter and Search Console account setup, and
repository tooling live here.

## Spec

### Development discipline

- Every change an agent makes to a tracked file is made in an
  isolated git worktree (`just worktree-create <branch>`) and lands
  through a pull request against `main`; the primary checkout is
  never edited directly. Maintainer exception: the maintainer MAY
  commit directly to `main` (for example by editing a file in the
  GitHub web editor), and such a commit is checked and deployed
  like any other push to `main`. Agents MUST NOT commit or push
  directly to `main`, even when acting on the maintainer's behalf.
- Spec changes flow through `/livespec:propose-change` →
  `/livespec:revise`.
- Every HTML page under `site/` is rendered from a Markdown source
  under `content/`; contributors edit the Markdown source, never the
  rendered HTML directly. Edits preserve the site's existing markup
  conventions, relative structure, and published URLs.
  Site-specific markup MAY be written as raw HTML inside the
  Markdown. An internal link in a Markdown source SHOULD target the
  linked page's Markdown source by relative path (for example
  `blog/index.md`), so the link also works when browsing `content/`
  on GitHub. Rendered HTML pages under `site/` are build output: they
  MUST be gitignored and MUST NOT be committed. Static assets under
  `site/` (`css/`, `CNAME`, `robots.txt`, `sitemap.xml`,
  `.nojekyll`) stay committed.

### Tooling and enforcement

- Any scripting the project needs is expressed as `just` recipes
  in the root `justfile`; helper scripts under `scripts/` are
  invoked only through `just` recipes. Scripting is kept minimal —
  the site itself needs none to be served; rendering runs only on
  contributor machines and in the GitHub Actions workflow.
- `just check` is the single check-aggregate command (see
  [Check-aggregate command](#check-aggregate-command)).

### Hooks and CI

- lefthook runs `00-install-worktree-pack` first in both
  `pre-commit` and `pre-push`, then `just check`.
- The GitHub Actions workflow runs `just check` before deploying;
  a failing check blocks deployment.

### Contributor workflow

- `AGENTS.md` (symlinked as `CLAUDE.md`) carries agent-facing
  operating instructions.
- Implementation work-items live in the
  `livespec-orchestrator-beads-fabro` ledger.
- Every website change is carried through to verified live
  publication: merge, confirm the deploy run for that exact commit
  succeeded, then fetch each changed public URL on
  `https://livespec-ai.org/` and confirm the change is live.
  Cloudflare may rewrite email links and inject scripts at the
  edge; live verification accounts for that.

## Contracts

### Contributor toolchain

Tools are pinned in `.mise.toml` and run via `mise exec --`:
`uv` (Python, for livespec dev-tooling and the site checks),
`just`, `lefthook`, and `pandoc` (Markdown rendering).
`just bootstrap` MUST install every pinned tool. Python dev
dependencies (`livespec-dev-tooling`) are pinned in
`pyproject.toml` / `uv.lock`. None of this toolchain is shipped to
visitors.

### Render, preview, and watch commands

- `just render` MUST render every `content/**/*.md` source to its
  page under `site/` with pandoc (GitHub-flavored Markdown input
  with YAML front matter and explicit heading attributes, without
  automatic heading identifiers; HTML5 output) and the one shared
  template `templates/page.html`. Per-page metadata (title,
  description, canonical path, Open Graph type, dates, GoatCounter
  path) comes from the source's YAML front matter. The template's
  internal links and stylesheet link MUST be computed per page so
  they take the form contracts.md §"URL surface" requires: the
  shortest relative path on every page, root-absolute on
  `/404.html`. Before rendering, `just render` MUST remove every
  previously rendered HTML page under `site/`, so a deleted or
  renamed source leaves no stale page.
- `just render` MUST rewrite every relative link whose path ends in
  `.md` (optionally followed by a `?query` or `#fragment`, which are
  kept) to the same path ending in `.html`, both in Markdown links
  and in `href` attributes of raw HTML in the source. It MUST NOT
  rewrite a link that has a URL scheme (such as `https:` or
  `mailto:`), a protocol-relative link (`//host/...`), or a
  root-absolute link (`/...`).
- `just preview` MUST run `just render`, print the `file://` URL
  of `site/index.html`, and open it with the platform opener
  (`open` on macOS, `xdg-open` on Linux).
- `just watch` MUST run `just render`, then poll `content/` and
  `templates/` about once per second and re-run `just render`
  whenever a file there changes, until interrupted. It MUST need
  nothing beyond the pinned toolchain and the POSIX shell
  utilities present on macOS and Ubuntu.
- No HTTP server is part of the contributor toolchain; local
  review opens rendered pages from the filesystem.

### Check-aggregate command

`just check` MUST first run `just render`, so it checks exactly the
pages a deploy of the same commit would publish, then runs, at
minimum:

1. **HTML validity** — every page under `site/` is valid HTML5.
2. **Site-wide link check** — every internal link, stylesheet, and
   fragment on every page under `site/` resolves; external links
   are checked with bounded concurrency and timeouts, where 404/410
   fails and 403/429/timeouts are reported as unverified rather
   than failing.
3. **Page contract check** — every page carries the metadata
   required by `contracts.md` §"Per-page HTML contract", and
   `sitemap.xml` lists exactly the published pages.

### Publishing

- The publishable site lives in the `site/` directory; only
  `site/` is deployed. Repository tooling, `SPECIFICATION/`, and
  `dev-tooling/` are never published.
- A GitHub Actions workflow deploys `site/` to GitHub Pages on
  every push to `main` (Pages source: GitHub Actions). The
  workflow's check job installs the pinned toolchain (including
  pandoc) through mise and runs `just check`; a failing check MUST
  block the deploy job. The deploy job MUST install the same pinned
  toolchain through mise and run `just render` on the pushed commit
  before uploading `site/`.
- `site/CNAME` contains `livespec-ai.org`, and the Pages custom
  domain is set to `livespec-ai.org` with HTTPS enforced.

## Constraints

### Repository layout

| Path | Purpose |
|---|---|
| `site/` | Everything published: rendered HTML (build output, gitignored), and committed `css/`, `robots.txt`, `sitemap.xml`, `CNAME`, `.nojekyll` |
| `site/blog/<slug>/index.html` | One rendered blog entry (from `content/blog/<slug>/index.md`) |
| `content/` | Markdown sources, one per rendered HTML page under `site/` (never published) |
| `templates/page.html` | The one shared pandoc page template (never published) |
| `SPECIFICATION/` | The livespec specification |
| `justfile`, `lefthook.yml`, `.mise.toml`, `pyproject.toml`, `scripts/` | Contributor tooling |

`site/.nojekyll` MUST exist so GitHub Pages serves files verbatim.

### DNS and Cloudflare

Mirrors the existing `thewoolleyweb.com` setup:

- The `livespec-ai.org` zone is on Cloudflare.
- The apex and `www` records point at GitHub Pages and are
  proxied through Cloudflare.
- Cloudflare SSL/TLS mode is Full (strict); "Always Use HTTPS" is
  on.
- `www` → apex redirect is a Cloudflare redirect rule.

### Traffic metrics and search console

- A GoatCounter site exists for `livespec-ai.org`; its site code
  is the one embedded in pages' count script and pixel URLs. The
  site code is public, not a secret.
- `livespec-ai.org` is verified as a Google Search Console
  property (DNS TXT verification through Cloudflare), and
  `https://livespec-ai.org/sitemap.xml` is submitted.

### Styling source

`site/css/style.css` starts from a copy of takahashi `default.css`
from `thewoolleyman/thewoolleyman`, keeping its credit comment, then
removes the fixed minimum width and adds the prose style.

## Scenarios

### Scenario: A merged change is published and verified live

Given a pull request that changes a Markdown source under `content/` or a file under `site/`

And `just check` passes

When the pull request is merged to `main`

Then the GitHub Actions deploy run for that merge commit succeeds

And fetching the changed page on `https://livespec-ai.org/` returns the new content

### Scenario: A broken internal link blocks the change

Given a page under `site/` links to a path that does not exist under `site/`

When a contributor runs `just check`

Then the check fails and names the referring page and the broken URL

### Scenario: Checking renders the pages first

Given a Markdown source under `content/` has been edited and `just render` has not been run

When a contributor runs `just check`

Then the pages are rendered from the edited source before any check runs

And the checks report on the newly rendered pages

### Scenario: A deleted source leaves no stale page

Given a Markdown source under `content/` was rendered and then deleted

When a contributor runs `just render`

Then no HTML page for the deleted source remains under `site/`

### Scenario: Internal .md links render as .html links

Given a Markdown source under `content/` links to `blog/index.md` in a Markdown link and to `the-journey-begins/index.md#intro` in a raw HTML `href`

And it links to `https://github.com/thewoolleyman/livespec/blob/main/README.md`

When a contributor runs `just render`

Then the rendered page links to `blog/index.html` and `the-journey-begins/index.html#intro`

And the external link to `README.md` on GitHub is unchanged

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

### Scenario: A contributor previews the rendered site locally

Given a contributor has edited a Markdown source under `content/`

When the contributor runs `just preview`

Then every page is re-rendered under `site/`

And the `file://` URL of `site/index.html` is printed and opened in the platform's default browser without starting an HTTP server

### Scenario: Watching re-renders a page when its source changes

Given a contributor is running `just watch`

When the contributor saves a change to a Markdown source under `content/` or to `templates/page.html`

Then within 3 seconds every affected page under `site/` is re-rendered from the saved files
