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

# Every check (SPECIFICATION/non-functional-requirements.md §"Check-aggregate command").
check:
    uv run python scripts/check-site.py

# Serve site/ locally at http://127.0.0.1:8000/ for a visual check.
serve:
    python3 -m http.server 8000 --bind 127.0.0.1 --directory site
