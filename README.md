# itil-automation-runbooks

A small Python CLI toolkit for ITIL service-management automation.
It uses the [Anthropic Claude API](https://docs.anthropic.com/) to triage
incidents, changes, and service requests, and ships with Markdown runbooks
that document each process.

## Quick Start

```bash
# 1. Clone & install
git clone https://github.com/Jacquesngw1/verbose-barnacle.git
cd verbose-barnacle
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. (Optional) Configure API key for live mode
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-...
```

Or use the Makefile:

```bash
make setup          # creates venv + installs deps
source .venv/bin/activate
```

## Usage

### Triage Classifier

Classify an incident, change, or service request:

```bash
python scripts/triage_classifier.py \
  --mode incident \
  --description "Auth service returning 503 errors for all users."
```

Supported modes: `incident`, `change`, `service_request`.

### Dry-Run Mode (no API key required)

Pass `--dry-run` or set `TRIAGE_DRY_RUN=1` to get deterministic sample
output without calling the Anthropic API:

```bash
python scripts/triage_classifier.py \
  --mode incident \
  --description "Test" \
  --dry-run
```

```bash
TRIAGE_DRY_RUN=1 python scripts/triage_classifier.py \
  --mode change \
  --description "Test"
```

### Incident Handler

```bash
python scripts/incident_handler.py --action create --description "DB timeout" --priority P2
python scripts/incident_handler.py --action list
```

### Change Handler

```bash
python scripts/change_handler.py --action create --description "Deploy v2" --type Standard --risk Low
python scripts/change_handler.py --action list
```

### Service Request Handler

```bash
python scripts/service_request_handler.py --action create --description "VPN access" --priority P3
python scripts/service_request_handler.py --action list
```

## Build / Verify

### Locally

```bash
make setup           # create venv and install deps
make lint            # compile-check all scripts
make smoke           # run classifier dry-run + handler list (no API key)
```

### CI (GitHub Actions)

The repository includes a `.github/workflows/ci.yml` workflow that runs
on every push and pull request to `main`. It:

1. Checks out the code.
2. Sets up Python 3.12.
3. Installs dependencies via `pip install -r requirements.txt`.
4. Runs `python -m compileall scripts/` to verify syntax.
5. Runs the triage classifier in `--dry-run` mode for each mode.
6. Runs `incident_handler.py --action list` as a basic handler smoke test.

No secrets or API keys are required for CI to pass.

## Project Structure

```
.
├── .github/workflows/ci.yml   # GitHub Actions CI
├── examples/usage.md           # Example commands
├── runbooks/
│   ├── incident_management.md
│   ├── change_management.md
│   └── service_request.md
├── scripts/
│   ├── triage_classifier.py
│   ├── incident_handler.py
│   ├── change_handler.py
│   └── service_request_handler.py
├── .env.example
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

## License

[MIT](LICENSE)