# livespec-website — agent instructions

This repository holds the livespec website. It is governed by livespec: a
living natural-language specification drives the implementation. The active
implementation plugin is `livespec-orchestrator-beads-fabro`.

## Messaging other agent sessions

Read the fleet's distributed SendMessage protocol (file
`distributed-sendmessage-protocol.md` in
<https://github.com/thewoolleyman/livespec-dev-tooling/tree/master/.ai>)
before messaging, asking, directing or answering another agent session on any
host, and before running `herdr pane send-text`, `herdr pane run`,
`herdr agent prompt` or `tmux send-keys` against a pane you did not create.
Prefer `SendMessage` (across machines via Remote Control) to message another
Claude session, because typed text can interrupt the maintainer. Typing into a
pane is still allowed and nothing blocks it; use it when necessary (a slash
command, a picker, a session `SendMessage` cannot reach, a Codex or pi seat)
(maintainer rulings 2026-11-14).

## Current state

The spec is seeded (`SPECIFICATION/`, template `livespec-with-diagrams`).
`.livespec.jsonc` selects `livespec-orchestrator-beads-fabro` with
`worktree_discipline.pack: required`. The site lives in `site/` (static HTML +
`css/style.css`). Every HTML page is rendered from a Markdown source in
`content/` by `just render` (pandoc through `templates/page.html`); edit the
Markdown, never the rendered HTML. Rendered pages are gitignored build output:
never commit them. `just preview` renders and opens the homepage from the
filesystem; `just watch` re-renders on change. `just check` renders, then
(`scripts/check-site.py`) gates the site locally via lefthook and in CI via
`.github/workflows/pages.yml`, whose deploy job renders `site/` again and
publishes it to GitHub Pages on every push to `main`. Factory dispatch (installation
Phase 6: GitHub App, credential wrapper, Fabro server) is deliberately
deferred by the maintainer; implementation happens in-session through
worktree PRs.

## Beads ledger

Work items live in the `livespec-website` family tenant (prefix `lsw`) on the
shared Dolt server. On a fresh clone, run `mise exec -- just beads-setup` once
(needs the Dolt tunnel on 127.0.0.1:3307 and `/usr/local/bin/with-livespec-env.sh`);
it regenerates the gitignored `.beads/metadata.json`. Run `bd` through the
wrapper: `/usr/local/bin/with-livespec-env.sh -- bd list`.

## Spec lifecycle

Once seeded, the specification is the source of truth. Change it only through
the livespec operations (`/livespec:propose-change`, `/livespec:critique`,
`/livespec:revise`), validate with `/livespec:doctor`, and use
`/livespec:next` and `/livespec:help` to orient. Implementation work-items
live in the orchestrator's ledger, not in ad-hoc checklists or handoff files.

## Toolchain

Tools are pinned in `.mise.toml` (uv, just, lefthook). Run commands through
mise, e.g. `mise exec -- just <recipe>`. `just bootstrap` syncs Python dev
dependencies, installs the worktree-discipline pack, and installs the git
hooks. The pack in `dev-tooling/` is materialized from the pinned
`livespec-dev-tooling` package and is gitignored; never copy or commit it.

## Repository mutations

After the initial setup commit, every tracked change an agent makes happens in
a dedicated git worktree and lands through a PR against `main`, never as a
direct edit on the primary checkout. Never bypass a rejecting hook.

Maintainer exception (2026-11-14): the maintainer may commit directly to
`main`, for example by editing a `content/` Markdown file in the GitHub web
editor; that push is checked and deployed like any other. Agents never commit
or push directly to `main`, even when acting on the maintainer's behalf. Expect
maintainer commits on `main` you did not author: rebase onto them.

## Working style

Read [`.ai/agent-working-style.md`](.ai/agent-working-style.md). In short: keep
going until everything is done or you are blocked on the maintainer; batch
blockers into one ask.

## PR process

Read [`.ai/pr-process.md`](.ai/pr-process.md) before opening or landing a PR.
In short: merge PRs automatically, without asking, once CI passes (rebase
merge, delete the branch); never merge on red. Until a CI workflow exists, a
PR with no checks counts as passing once the local hooks pass.

## Secrets

Never read, print, or commit secret values. Credentials are injected at run
time by the project's credential wrapper (declared in `.livespec.jsonc` as
`credential_wrapper`), and presence is checked by byte count only.

## Instruction files

`CLAUDE.md` is a symlink to this file. Edit `AGENTS.md` only.
