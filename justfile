import? 'dev-tooling/worktree.just'
import? 'dev-tooling/branch-protection.just'

set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

bootstrap:
    uv sync --all-groups
    just install-worktree-pack
    lefthook install

install-worktree-pack:
    uv run python -m livespec_dev_tooling.install_worktree_pack
