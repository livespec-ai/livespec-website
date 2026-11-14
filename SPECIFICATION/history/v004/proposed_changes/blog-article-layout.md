---
topic: blog-article-layout
author: claude-opus-5-5
created_at: 2026-11-14T03:09:36Z
---

## Proposal: Blog entries use a dedicated article layout with author and date byline

### Target specification files

- SPECIFICATION/spec.md
- SPECIFICATION/contracts.md
- SPECIFICATION/constraints.md
- SPECIFICATION/scenarios.md

### Summary

Blog entry pages get an article layout distinct from the takahashi centered/menu look: the title, an author byline, and the publication date sit together in an article header that shares the readable prose column, following modern long-form reading conventions. Every entry, including the launch placeholder, shows the author and date in addition to the title, and the placeholder body is filled with clearly marked humorous AI-themed filler text so the layout can be judged with realistic length.

### Motivation

Maintainer feedback: the blog formatting does not match the seed intent, which called for additional styling beyond thewoolleyweb.com's centered menu styles. The current entry reuses the centered grey takahashi title band and shows only a bare 'Published' line. Standard blog metadata (author and date) is missing. Strict left-justification is not the point; modern readable article best practices are.

### Proposed Changes

spec.md §Blog: replace the entry-page bullet with: Each entry page MUST present an article header containing the entry title, an author byline ("Chad Woolley", linking to https://thewoolleyweb.com/), and the publication date, followed by the body prose, and MUST link back to `/blog/` and `/`. Replace the placeholder bullet with: At launch the blog contains exactly one entry, a clearly marked placeholder on the theme of the author's journey toward the two project goals. Its body MUST be several paragraphs of humorous AI-themed lorem-ipsum-style filler text, so that the article layout can be reviewed at realistic length, until the author writes the real content.

spec.md §Visual style: add a bullet: Blog entry pages use an **article style** added for this site: the title, byline, and body share one readable column; the title is large and bold but start-aligned with the body rather than set in a centered band; the byline is visually subordinate to the title; body text follows modern long-form reading conventions. Amend the prose-style bullet to read "start-aligned (left-aligned in English)" instead of "left-justified", and append ", except as the article style below specifies" to the takahashi navigation-and-heading bullet.

contracts.md §Blog entry contract: add: Each blog entry page MUST wrap the entry in an `<article>` element whose `<header>` contains the entry's `<h1>` title and a byline naming the author and the publication `<time datetime="YYYY-MM-DD">`. Each entry page MUST include `<meta name="author" content="Chad Woolley">` and `<meta property="article:author" content="https://thewoolleyweb.com/">`.

constraints.md §Styling: replace the prose bullet with: Prose and article blocks MUST be start-aligned (never fully justified), normal weight, with a line height of about 1.6 to 1.75 and a maximum line length of about 70 characters. Add: The blog article header MUST place title, byline, and body in the same column; the byline MUST use a smaller size and a muted grey that still meets WCAG 2.2 AA contrast.

scenarios.md §Visitor browses the blog: change the arrival step to: Then the visitor arrives at `/blog/<slug>/` showing the entry's title, author, publication date, and placeholder text. §Visitor uses a phone: change the last step to: And prose paragraphs are start-aligned in a single readable column.
