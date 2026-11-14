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

# Every check (the check-aggregate command in SPECIFICATION/non-functional-requirements.md).
check:
    uv run python scripts/check-site.py

# Serve site/ locally at http://127.0.0.1:8000/ for a visual check.
serve:
    python3 -m http.server 8000 --bind 127.0.0.1 --directory site

# Set up the beads ledger on a fresh clone: regenerate the gitignored
# .beads/metadata.json from .beads/config.yaml plus the tenant's project_id.
# Needs the Dolt tunnel on 127.0.0.1:3307 and the family credential wrapper.
beads-setup:
    python3 scripts/beads-setup.py
