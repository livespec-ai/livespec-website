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

- Every change to a tracked file is made in an isolated git
  worktree (`just worktree-create <branch>`) and lands through a
  pull request against `main`; the primary checkout is never
  edited directly.
- Spec changes flow through `/livespec:propose-change` →
  `/livespec:revise`.
- Pages are hand-authored HTML; edits preserve the site's existing
  markup conventions, relative structure, and published URLs.

### Tooling and enforcement

- Any scripting the project needs is expressed as `just` recipes
  in the root `justfile`; ad-hoc scripts outside `just` are not
  added. Scripting is kept minimal — the site itself needs none to
  be served.
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
`uv` (Python, for livespec dev-tooling only), `just`, and
`lefthook`. Python dev dependencies (`livespec-dev-tooling`) are
pinned in `pyproject.toml` / `uv.lock`. None of this toolchain is
shipped to visitors.

### Check-aggregate command

`just check` runs, at minimum:

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
  every push to `main` (Pages source: GitHub Actions), with no
  build step beyond uploading the directory.
- `site/CNAME` contains `livespec-ai.org`, and the Pages custom
  domain is set to `livespec-ai.org` with HTTPS enforced.

## Constraints

### Repository layout

| Path | Purpose |
|---|---|
| `site/` | Everything published: HTML, `css/`, `robots.txt`, `sitemap.xml`, `CNAME`, `404.html`, `.nojekyll` |
| `site/blog/<slug>/index.html` | One blog entry |
| `SPECIFICATION/` | The livespec specification |
| `justfile`, `lefthook.yml`, `.mise.toml`, `pyproject.toml` | Contributor tooling |

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

Given a pull request that changes a page under `site/`

And `just check` passes

When the pull request is merged to `main`

Then the GitHub Actions deploy run for that merge commit succeeds

And fetching the changed page on `https://livespec-ai.org/` returns the new content

### Scenario: A broken internal link blocks the change

Given a page under `site/` links to a path that does not exist under `site/`

When a contributor runs `just check`

Then the check fails and names the referring page and the broken URL
