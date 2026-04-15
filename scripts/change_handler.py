#!/usr/bin/env python3
"""ITIL Change Handler – create and list change requests.

Change records are stored as JSON files under the ``.changes/`` directory.
"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

CHANGES_DIR = os.path.join(os.getcwd(), ".changes")


def _ensure_dir() -> None:
    os.makedirs(CHANGES_DIR, exist_ok=True)


def create_change(description: str, change_type: str, risk: str) -> dict:
    _ensure_dir()
    change_id = f"CHG-{uuid.uuid4().hex[:8].upper()}"
    change = {
        "id": change_id,
        "description": description,
        "type": change_type,
        "risk": risk,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path = os.path.join(CHANGES_DIR, f"{change_id}.json")
    with open(path, "w") as fh:
        json.dump(change, fh, indent=2)
    return change


def list_changes() -> list[dict]:
    _ensure_dir()
    changes: list[dict] = []
    for fname in sorted(os.listdir(CHANGES_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(CHANGES_DIR, fname)) as fh:
                changes.append(json.load(fh))
    return changes


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="ITIL Change Handler")
    parser.add_argument(
        "--action",
        required=True,
        choices=["create", "list"],
        help="Action to perform.",
    )
    parser.add_argument("--description", help="Change description (for create).")
    parser.add_argument(
        "--type",
        dest="change_type",
        default="Standard",
        help="Change type (default: Standard).",
    )
    parser.add_argument(
        "--risk",
        default="Low",
        help="Risk level (default: Low).",
    )

    args = parser.parse_args(argv)

    if args.action == "create":
        if not args.description:
            parser.error("--description is required for create action")
        result = create_change(args.description, args.change_type, args.risk)
        print(json.dumps(result, indent=2))
    elif args.action == "list":
        changes = list_changes()
        print(json.dumps(changes, indent=2))


if __name__ == "__main__":
    main()
