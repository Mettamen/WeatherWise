# API agreement worksheet

**Owners: Sam, Metta and Shreshta. No endpoints or payloads are implemented yet.**

Sam should maintain this document after all three agree. Resolve the items below before implementing the relevant features.

## Endpoint planning

| Feature | Sam defines | Metta supplies | Shreshta needs |
| --- | --- | --- | --- |
| Login/account | Method, URL, credentials, token/session and errors | No calculation needed | Login form and authenticated state |
| Catalog | Locations, occupations and condition identifiers | Supported conditions and required weights | Dropdown/checklist options |
| Profile | Required fields, validation, get/save/delete behaviour | Fields required for risk calculations | Form labels, defaults and error messages |
| Routines | Time-block schema, availability and timezone | Constraints required by the scheduler | Routine editor and availability controls |
| Weather | Source, timestamp, forecast horizon, units, freshness and missing data | Required environmental measurements | Hourly forecast and source/freshness indicators |
| Dashboard | Route, response structure and access rules | Risk, reasons, advice and windows | Complete dashboard example |
| Alerts | Read/history/preferences and delivery status | Event rules, severity and deduplication | Alert list and notification settings |
| Outdoor windows | Request/response and storage, if needed | Feasible window ranking with explanations | Time-window cards and selection behaviour |

## Questions to settle together

- Which profile fields are required for the first version?
- What are the exact field names and units?
- Will timestamps use ISO 8601 with an explicit offset? How is India local time represented?
- Which risk levels and score boundaries are agreed?
- How is a missing measurement represented, rather than mistaken for zero?
- How are synthetic, live and stale data labelled?
- What is the response when no activity window fits?
- How are authentication errors and validation errors formatted?
- Which responses can be cached, and which contain private profile information?

## Contract change process

1. Propose the field/endpoint change with an example and reason.
2. All affected owners agree.
3. Sam updates contracts and API documentation; Metta updates calculation inputs/outputs if affected.
4. Update Shreshta's mock JSON together with the contract.
5. Implement and verify integration.

Add actual endpoint tables and example JSON here when the team agrees. Empty schema/mock files are intentionally not populated yet.
