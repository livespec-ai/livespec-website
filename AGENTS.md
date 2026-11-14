# livespec-website — agent instructions

This repository holds the livespec website. It is governed by livespec: a
living natural-language specification drives the implementation. The active
implementation plugin is `livespec-orchestrator-beads-fabro`.

## Messaging other agent sessions

Read the fleet's distributed SendMessage protocol
(<https://github.com/thewoolleyman/livespec-dev-tooling/blob/master/.ai/distributed-sendmessage-protocol.md>)
before messaging, asking, directing or answering another agent session on any
host, and before running `herdr pane send-text`, `herdr pane run`,
`herdr agent prompt` or `tmux send-keys` against a pane you did not create.
Claude sessions talk through `SendMessage` (across machines via Remote
Control), never by typing into each other's panes (maintainer ruling
2026-11-14).

## Current state

The spec is seeded (`SPECIFICATION/`, template `livespec-with-diagrams`).
`.livespec.jsonc` selects `livespec-orchestrator-beads-fabro` with
`worktree_discipline.pack: required`. The site lives in `site/` (pure HTML +
`css/style.css`); `just check` (`scripts/check-site.py`) gates it locally via
lefthook and in CI via `.github/workflows/pages.yml`, which also deploys
`site/` to GitHub Pages on push to `main`. Factory dispatch (installation
Phase 6: GitHub App, credential wrapper, Fabro server) is deliberately
deferred by the maintainer; implementation happens in-session through
worktree PRs.

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

After the initial setup commit, every tracked change happens in a dedicated
git worktree and lands through a PR against `main`, never as a direct edit on
the primary checkout. Never bypass a rejecting hook.

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
