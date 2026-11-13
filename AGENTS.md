# livespec-website — agent instructions

This repository holds the livespec website. It is governed by livespec: a
living natural-language specification drives the implementation. The active
implementation plugin is `livespec-orchestrator-beads-fabro`.

## Current state

livespec plugins are installed at project scope (`.claude/settings.json`,
pinned to the `release` channel, kept current by the `SessionStart` updater
hook). The spec has not been seeded yet: there is no `SPECIFICATION/` tree and
no `.livespec.jsonc`. The next step is `/livespec:seed`, an attended interview
with the maintainer. Do not hand-create `.livespec.jsonc` or spec files before
seed runs. After seed, merge `implementation.plugin` and `worktree_discipline`
into `.livespec.jsonc`.

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

## Secrets

Never read, print, or commit secret values. Credentials are injected at run
time by the project's credential wrapper (declared in `.livespec.jsonc` as
`credential_wrapper`), and presence is checked by byte count only.

## Instruction files

`CLAUDE.md` is a symlink to this file. Edit `AGENTS.md` only.
