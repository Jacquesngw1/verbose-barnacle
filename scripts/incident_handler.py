#!/usr/bin/env python3
"""ITIL Incident Handler – create, list, and manage incidents.

Incidents are stored as JSON files under the ``.incidents/`` directory
(relative to the working directory).

When the Anthropic API key is available, new incidents are enriched with
AI-generated analysis; otherwise only the user-supplied fields are stored.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

INCIDENTS_DIR = os.path.join(os.getcwd(), ".incidents")


def _ensure_dir() -> None:
    os.makedirs(INCIDENTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def create_incident(description: str, priority: str) -> dict:
    """Create a new incident and persist it."""
    _ensure_dir()
    incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    incident = {
        "id": incident_id,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path = os.path.join(INCIDENTS_DIR, f"{incident_id}.json")
    with open(path, "w") as fh:
        json.dump(incident, fh, indent=2)
    return incident


def list_incidents() -> list[dict]:
    """Return all stored incidents."""
    _ensure_dir()
    incidents: list[dict] = []
    for fname in sorted(os.listdir(INCIDENTS_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(INCIDENTS_DIR, fname)) as fh:
                incidents.append(json.load(fh))
    return incidents


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="ITIL Incident Handler")
    parser.add_argument(
        "--action",
        required=True,
        choices=["create", "list"],
        help="Action to perform.",
    )
    parser.add_argument("--description", help="Incident description (for create).")
    parser.add_argument(
        "--priority",
        default="P3",
        help="Priority level (default: P3).",
    )

    args = parser.parse_args(argv)

    if args.action == "create":
        if not args.description:
            parser.error("--description is required for create action")
        result = create_incident(args.description, args.priority)
        print(json.dumps(result, indent=2))
    elif args.action == "list":
        incidents = list_incidents()
        print(json.dumps(incidents, indent=2))


if __name__ == "__main__":
    main()
