"""Set up the beads ledger on a fresh clone of this repo (run via `just beads-setup`).

A clone carries only the committed `.beads/config.yaml` and `.beads/.gitignore`.
`bd` also needs the machine-local, gitignored `.beads/metadata.json`; without it
`bd bootstrap` would create an unrelated local database instead of using the
shared Dolt tenant. This script regenerates that file from `config.yaml`, then
fills in the tenant's `project_id` read back from the server, so the workspace
identity matches every other clone. It is idempotent and writes no secret; the
tenant password is injected by the `credential_wrapper` in `.livespec.jsonc`.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEADS = ROOT / ".beads"


def read_config() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in (BEADS / "config.yaml").read_text().splitlines():
        m = re.match(r"^(dolt\.[\w-]+):\s*(.+?)\s*$", line)
        if m:
            values[m.group(1)] = m.group(2).strip("\"'")
    return values


def credential_wrapper() -> list[str]:
    text = (ROOT / ".livespec.jsonc").read_text()
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    return json.loads(text)["credential_wrapper"]


def main() -> int:
    cfg = read_config()
    if cfg.get("dolt.mode") != "server":
        print("beads-setup: .beads/config.yaml is not a server-mode tenant", file=sys.stderr)
        return 1
    meta_path = BEADS / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    meta.update({
        "database": "dolt",
        "backend": "dolt",
        "dolt_mode": "server",
        "dolt_server_host": cfg["dolt.server-host"],
        "dolt_server_user": cfg["dolt.server-user"],
        "dolt_database": cfg["dolt.database"],
    })
    meta.pop("dolt_server_port", None)  # deprecated: bd reads the port from config.yaml
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    BEADS.chmod(0o700)

    query = "select value from metadata where `key`='_project_id'"
    out = subprocess.run([*credential_wrapper(), "bd", "sql", "--json", query],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        print(f"beads-setup: could not reach tenant {cfg['dolt.database']} "
              f"(is the Dolt tunnel up on {cfg['dolt.server-host']}:{cfg['dolt.server-port']}?)\n"
              f"{out.stderr.strip()}", file=sys.stderr)
        return 1
    rows = json.loads(out.stdout)
    if rows:
        meta["project_id"] = rows[0]["value"]
        meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    subprocess.run(["git", "config", "beads.role", "maintainer"], cwd=ROOT, check=True)
    print(f"beads-setup: .beads/metadata.json ready for tenant {cfg['dolt.database']} "
          f"(project_id {meta.get('project_id', 'unset')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
