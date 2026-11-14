import? 'dev-tooling/worktree.just'
import? 'dev-tooling/branch-protection.just'

set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

bootstrap:
    mise install
    uv sync --all-groups
    just install-worktree-pack
    lefthook install

install-worktree-pack:
    uv run python -m livespec_dev_tooling.install_worktree_pack

# Render, then run every check (the check-aggregate command in SPECIFICATION/non-functional-requirements.md).
check: render
    uv run python scripts/check-site.py

# Render every content/**/*.md source to its page under site/ with pandoc (gitignored build output).
render:
    uv run python scripts/render.py

# Render, then print and open the file:// URL of the homepage (no HTTP server).
preview: render
    #!/usr/bin/env bash
    set -euo pipefail
    url="file://{{justfile_directory()}}/site/index.html"
    echo "$url"
    case "$(uname)" in
      Darwin) open "$url" ;;
      *) xdg-open "$url" ;;
    esac

# Re-render whenever a Markdown source or the template changes (polls once a second; Ctrl-C to stop).
watch: render
    #!/usr/bin/env bash
    set -euo pipefail
    touch .render-stamp
    echo "watch: polling content/ and templates/ for changes (Ctrl-C to stop)"
    while sleep 1; do
      if [ -n "$(find content templates -newer .render-stamp -print -quit)" ]; then
        touch .render-stamp
        just render
      fi
    done

# Set up the beads ledger on a fresh clone: regenerate the gitignored
# .beads/metadata.json from .beads/config.yaml plus the tenant's project_id.
# Needs the Dolt tunnel on 127.0.0.1:3307 and the family credential wrapper.
beads-setup:
    python3 scripts/beads-setup.py
