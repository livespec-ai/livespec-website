# livespec-ai.com — the livespec project website — specification overview

This `SPECIFICATION/` directory holds the living specification for
the livespec project website at `https://livespec-ai.com`, governed
by livespec's propose-change/revise loop. The
`livespec-with-diagrams` template ships six spec files plus the
`proposed_changes/` and `history/` machinery:

- `spec.md` — what the site is: intent, pages (homepage and blog),
  visual style, Definition of Done, non-goals.
- `contracts.md` — the URL surface and the per-page HTML, blog
  entry, and sitemap contracts.
- `constraints.md` — visitor-observable constraints: pure static
  HTML, hosting and domain, styling, GoatCounter traffic metrics,
  SEO.
- `non-functional-requirements.md` — how the site is built,
  checked, and published: `just` recipes, `just check`, GitHub
  Pages deployment from `site/`, Cloudflare DNS, GoatCounter and
  Search Console setup, repository layout.
- `scenarios.md` — Gherkin acceptance scenarios for visitors.
- `README.md` (this file) — overview and entry point.

## Conventions

- Every spec file uses BCP 14 / RFC 2119 normative language
  (`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, `OPTIONAL`).
- `scenarios.md` puts each Gherkin step on its own line, preceded
  and followed by a blank line; no fenced code blocks for Gherkin.
- Cross-file references use `[link text](relative/path.md#section-name)`.

## Diagram conventions

Mermaid is the standard diagram format, authored as fenced
`mermaid` blocks inside the markdown spec files. A diagram that
needs another tool is rendered outside livespec and committed as an
image next to the markdown that references it.

## Lifecycle

Mutations to this `SPECIFICATION/` flow through
`/livespec:propose-change` → `/livespec:revise` (or
`/livespec:critique`). Hand-edits outside that loop are caught by
the doctor static phase's `out-of-band-edits` check.

## History

Past versions live under `history/v001/` through `history/vN/`.
`prune-history` (when invoked) consolidates older versions into a
`PRUNED_HISTORY.json` marker preserving the audit trail.
