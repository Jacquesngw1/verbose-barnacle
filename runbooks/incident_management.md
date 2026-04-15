# Incident Management Runbook

## Purpose
Guide first-responders through the ITIL incident management lifecycle.

## Triage
1. Receive and log the incident.
2. Run the triage classifier:
   ```bash
   python scripts/triage_classifier.py --mode incident --description "<description>"
   ```
3. Review the suggested **category** and **priority**.

## Investigation
- Check monitoring dashboards for related alerts.
- Review recent deployments and change records.
- Gather logs from affected services.

## Resolution
1. Apply a workaround or fix.
2. Verify the service is restored.
3. Update the incident record:
   ```bash
   python scripts/incident_handler.py --action create --description "<resolution notes>" --priority P2
   ```

## Closure
- Confirm with the reporter that the issue is resolved.
- Document lessons learned.
- Schedule a post-incident review if severity ≤ P2.
