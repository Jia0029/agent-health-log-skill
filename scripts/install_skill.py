#!/usr/bin/env python3
"""Install the Agent Health Log skill package into common agent skill paths."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


TARGETS = {
    "agents-user": Path.home() / ".agents" / "skills",
    "agents-project": Path.cwd() / ".agents" / "skills",
    "claude-personal": Path.home() / ".claude" / "skills",
    "claude-project": Path.cwd() / ".claude" / "skills",
    "vscode-project": Path.cwd() / ".agents" / "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Agent Health Log Skill.")
    parser.add_argument(
        "--target",
        required=True,
        choices=sorted(TARGETS),
        help="Installation target.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing installed skill directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source = repo_root / "skills" / "agent-health-log"
    target_root = TARGETS[args.target]
    destination = target_root / "agent-health-log"

    if not source.is_dir():
        print(f"Error: skill package not found: {source}")
        return 1

    if destination.exists():
        if not args.force:
            print(f"Error: destination already exists: {destination}")
            print("Re-run with --force to replace it.")
            return 1
        shutil.rmtree(destination)

    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    print(f"Installed agent-health-log skill to: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

