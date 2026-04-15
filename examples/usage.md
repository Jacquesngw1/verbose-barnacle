# Examples

## Triage Classifier

### Classify an incident
```bash
python scripts/triage_classifier.py \
  --mode incident \
  --description "Auth service returning 503 errors for all users."
```

### Classify a change request
```bash
python scripts/triage_classifier.py \
  --mode change \
  --description "Upgrade PostgreSQL from 14 to 16 on prod cluster."
```

### Classify a service request
```bash
python scripts/triage_classifier.py \
  --mode service_request \
  --description "New hire needs VPN and GitHub access."
```

### Dry-run mode (no API key required)
```bash
python scripts/triage_classifier.py \
  --mode incident \
  --description "Test" \
  --dry-run
```

## Incident Handler

### Create an incident
```bash
python scripts/incident_handler.py \
  --action create \
  --description "Database timeout on prod" \
  --priority P2
```

### List incidents
```bash
python scripts/incident_handler.py --action list
```

## Change Handler

### Create a change
```bash
python scripts/change_handler.py \
  --action create \
  --description "Deploy v2.3.0 to production" \
  --type Standard \
  --risk Low
```

### List changes
```bash
python scripts/change_handler.py --action list
```

## Service Request Handler

### Create a service request
```bash
python scripts/service_request_handler.py \
  --action create \
  --description "Need access to analytics dashboard" \
  --priority P3
```

### List service requests
```bash
python scripts/service_request_handler.py --action list
```
