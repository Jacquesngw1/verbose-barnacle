# Change Management Runbook

## Purpose
Ensure changes to production systems follow a controlled, auditable process.

## Request
1. Submit a change request:
   ```bash
   python scripts/change_handler.py --action create --description "<change details>" --type Standard --risk Low
   ```
2. Classify the change with the triage classifier:
   ```bash
   python scripts/triage_classifier.py --mode change --description "<change details>"
   ```

## Approval
- **Standard** changes: auto-approved if low risk.
- **Normal** changes: require Change Advisory Board (CAB) approval.
- **Emergency** changes: require expedited approval from the change manager.

## Implementation
1. Schedule a maintenance window.
2. Execute the change per the implementation plan.
3. Validate success criteria.

## Review
- Confirm the change achieved its objectives.
- Close the change record.
- Document any deviations from the plan.
