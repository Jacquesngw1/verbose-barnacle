#!/usr/bin/env python3
"""ITIL Triage Classifier – classifies incidents, changes, or service requests.

Uses the Anthropic Claude API to analyse a description and return structured
JSON with recommended category, priority, and next steps.

Dry-run mode
------------
When the ``--dry-run`` flag is passed **or** the ``TRIAGE_DRY_RUN=1``
environment variable is set, the script returns deterministic sample JSON
without making any network calls.  This is useful for CI smoke-tests and
local development without an API key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Dry-run sample responses (one per mode)
# ---------------------------------------------------------------------------

_DRY_RUN_RESPONSES: dict[str, dict] = {
    "incident": {
        "mode": "incident",
        "category": "Application",
        "priority": "P2",
        "summary": "Dry-run: simulated incident triage",
        "next_steps": [
            "Verify service health",
            "Check recent deployments",
            "Escalate to on-call engineer",
        ],
    },
    "change": {
        "mode": "change",
        "category": "Standard",
        "risk": "Low",
        "summary": "Dry-run: simulated change triage",
        "next_steps": [
            "Submit change request",
            "Obtain CAB approval",
            "Schedule maintenance window",
        ],
    },
    "service_request": {
        "mode": "service_request",
        "category": "Access Management",
        "priority": "P3",
        "summary": "Dry-run: simulated service-request triage",
        "next_steps": [
            "Verify requester identity",
            "Provision access",
            "Notify requester",
        ],
    },
}

VALID_MODES = list(_DRY_RUN_RESPONSES.keys())

# ---------------------------------------------------------------------------
# Anthropic helper
# ---------------------------------------------------------------------------


def _classify_with_anthropic(mode: str, description: str) -> dict:
    """Call the Anthropic API and return parsed JSON."""
    import anthropic  # imported here so dry-run never needs the SDK

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY from env

    system_prompt = (
        f"You are an ITIL triage assistant. Classify the following {mode} "
        "description and return ONLY valid JSON with keys: mode, category, "
        "priority (or risk for changes), summary, and next_steps (a list)."
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": description}],
    )

    # Claude returns text; extract the first text block
    text = message.content[0].text
    return json.loads(text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _is_dry_run(args: argparse.Namespace) -> bool:
    return args.dry_run or os.environ.get("TRIAGE_DRY_RUN", "0") == "1"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="ITIL Triage Classifier – classify incidents, changes, "
        "or service requests using Claude.",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=VALID_MODES,
        help="Triage mode: incident | change | service_request",
    )
    parser.add_argument(
        "--description",
        required=True,
        help="Free-text description of the issue or request.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Return deterministic sample output without calling the API. "
        "Also enabled by setting TRIAGE_DRY_RUN=1.",
    )

    args = parser.parse_args(argv)

    if _is_dry_run(args):
        result = _DRY_RUN_RESPONSES[args.mode]
    else:
        result = _classify_with_anthropic(args.mode, args.description)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
