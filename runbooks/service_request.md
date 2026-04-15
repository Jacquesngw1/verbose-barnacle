# Service Request Runbook

## Purpose
Handle routine user service requests efficiently.

## Intake
1. Log the service request:
   ```bash
   python scripts/service_request_handler.py --action create --description "<request details>"
   ```
2. Classify the request:
   ```bash
   python scripts/triage_classifier.py --mode service_request --description "<request details>"
   ```

## Fulfilment
- Follow the prescribed fulfilment procedure for the request category.
- Common categories:
  - **Access Management** – provision/revoke access per IAM policy.
  - **Hardware** – raise a procurement ticket.
  - **Software** – install or licence the requested software.

## Closure
- Notify the requester that the request has been fulfilled.
- Close the service request record.
