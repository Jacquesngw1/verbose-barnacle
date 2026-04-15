VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: setup lint smoke clean

## Create virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## Run basic lint (syntax check)
lint:
	$(PYTHON) -m compileall scripts/

## Run smoke tests (no API key required)
smoke:
	$(PYTHON) scripts/triage_classifier.py --mode incident --description "smoke test" --dry-run
	$(PYTHON) scripts/triage_classifier.py --mode change --description "smoke test" --dry-run
	$(PYTHON) scripts/triage_classifier.py --mode service_request --description "smoke test" --dry-run
	$(PYTHON) scripts/incident_handler.py --action list

## Remove virtual environment and data directories
clean:
	rm -rf $(VENV) .incidents .changes .service_requests
