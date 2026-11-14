# livespec-ai.org — the livespec project website

## Project intent

`livespec-ai.org` is a minimal, pure-HTML public website for the
livespec project, authored by Chad Woolley ("thewoolleyman"). It
introduces the author, states the project's goals, summarizes the
project's current high-level state by linking out to the livespec
repositories, and hosts a blog chronicling the author's journey
exploring those goals.

livespec is presented as an **experimental work in progress**
pursuing two goals:

1. **A circular feedback loop between specification and
   implementation** — the specification drives the implementation,
   and observations of the implementation feed back into the
   specification through governed revision.
2. **Turning every quality dial as close to 11 as possible** within
   cost and speed constraints — an explicit engagement with the
   "fast, cheap, right: pick two" triangle.

## Architecture

The site is a set of hand-authored static HTML pages plus one
shared stylesheet, served by GitHub Pages behind Cloudflare. There
is no build step, no client-side framework, and no server-side
code.

```mermaid
flowchart LR
    visitor[Visitor browser] -->|HTTPS| cf[Cloudflare proxy<br/>livespec-ai.org]
    cf --> pages[GitHub Pages]
    repo[livespec-ai/livespec-website<br/>site/ directory] -->|deploy on push to main| pages
    home[Homepage] -.links to.-> gh[livespec repos on GitHub<br/>READMEs, docs, SPECIFICATIONs]
```

### Pages

The site has exactly two content areas at launch:

- **Homepage** at `/` (see [Homepage](#homepage)).
- **Blog** at `/blog/` (see [Blog](#blog)).

### Homepage

The homepage MUST contain, in this order:

1. **Author introduction** — a short paragraph introducing Chad
   Woolley ("thewoolleyman") with links to
   `https://thewoolleyweb.com/` and `https://github.com/thewoolleyman`.
2. **Project goals** — a statement that livespec is an
   experimental work in progress around the two goals named in
   [Project intent](#project-intent), each explained in no more than
   a short paragraph. The quality-dials goal MUST name the
   fast/cheap/right "pick two" triangle.
3. **Project state** — a high-level summary of where livespec
   currently stands. This section MUST rely primarily on links to
   existing content in the livespec GitHub repositories (READMEs,
   `docs/`, and `SPECIFICATION/` trees) and MUST NOT duplicate that
   content beyond a sentence or two of framing per link. At minimum
   it MUST link to the core `thewoolleyman/livespec` repository's
   README, its installation documentation, and its `SPECIFICATION/`
   tree.
4. **Blog link** — a link to `/blog/`.

### Blog

The blog lives under `/blog/`:

- `/blog/` is an index page listing every published entry, newest
  first, each with its title (linked), publication date, and an
  optional one-sentence summary.
- Each entry lives at `/blog/<slug>/`, where `<slug>` is a
  lowercase, hyphen-separated identifier that never changes after
  publication.
- Each entry page shows its title, publication date, and body
  prose, and links back to `/blog/` and `/`.
- At launch the blog contains exactly one entry, a clearly marked
  **placeholder** whose content the author fleshes out later. The
  placeholder's theme is the author's journey toward the two
  project goals.

The blog's subject is the author's journey exploring the two
project goals.

### Visual style

The visual style derives from thewoolleyweb.com's "takahashi"
stylesheet (`default.css` in `thewoolleyman/thewoolleyman`): big
letters, greyscale only, black header band, grey content area,
bold link-heavy navigation headings.

- Navigation and heading content (site title, section headings,
  link lists) uses the takahashi look: large, bold, centered.
- Prose content (homepage paragraphs, blog entry bodies) uses a
  **prose style** added for this site: left-justified, normal
  font weight, comfortable line height, and constrained to a
  readable line length.

The normative palette, font, and prose-measure rules live in
[constraints.md](constraints.md#styling).

## Definition of Done

A livespec-website change MUST satisfy both parts of this DoD.

Before merge:

- The spec change MUST flow through the propose-change/revise
  loop, with no out-of-band edits.
- Every page MUST conform to [contracts.md](contracts.md) and
  [constraints.md](constraints.md).
- The site-wide link check MUST pass (see
  [non-functional-requirements.md](non-functional-requirements.md)).
- The doctor static phase MUST pass against the working spec.

After merge:

- The change MUST be verified live on `https://livespec-ai.org/`
  per [non-functional-requirements.md](non-functional-requirements.md#contributor-workflow).
  A change is not done until that verification succeeds.

## Non-goals

- No JavaScript framework, bundler, transpiler, or static-site
  generator.
- No user accounts, comments, search, or server-side code.
- No duplication of livespec documentation already maintained in
  the livespec repositories.
- No color theme or dark mode at launch.
