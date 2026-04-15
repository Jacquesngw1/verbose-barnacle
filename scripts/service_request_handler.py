#!/usr/bin/env python3
"""ITIL Service Request Handler – create and list service requests.

Service request records are stored as JSON files under the
``.service_requests/`` directory.
"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

SERVICE_REQUESTS_DIR = os.path.join(os.getcwd(), ".service_requests")


def _ensure_dir() -> None:
    os.makedirs(SERVICE_REQUESTS_DIR, exist_ok=True)


def create_request(description: str, priority: str) -> dict:
    _ensure_dir()
    req_id = f"SR-{uuid.uuid4().hex[:8].upper()}"
    request = {
        "id": req_id,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path = os.path.join(SERVICE_REQUESTS_DIR, f"{req_id}.json")
    with open(path, "w") as fh:
        json.dump(request, fh, indent=2)
    return request


def list_requests() -> list[dict]:
    _ensure_dir()
    requests: list[dict] = []
    for fname in sorted(os.listdir(SERVICE_REQUESTS_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(SERVICE_REQUESTS_DIR, fname)) as fh:
                requests.append(json.load(fh))
    return requests


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="ITIL Service Request Handler")
    parser.add_argument(
        "--action",
        required=True,
        choices=["create", "list"],
        help="Action to perform.",
    )
    parser.add_argument("--description", help="Request description (for create).")
    parser.add_argument(
        "--priority",
        default="P3",
        help="Priority level (default: P3).",
    )

    args = parser.parse_args(argv)

    if args.action == "create":
        if not args.description:
            parser.error("--description is required for create action")
        result = create_request(args.description, args.priority)
        print(json.dumps(result, indent=2))
    elif args.action == "list":
        requests = list_requests()
        print(json.dumps(requests, indent=2))


if __name__ == "__main__":
    main()
