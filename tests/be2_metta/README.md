# Metta's engine tests

**Owner: Metta.** Implement tests independently of HTTP and the database.

| File | Cases to cover |
| --- | --- |
| `test_risk.py` | Exact risk-band boundaries, no-hazard cases, sensitivity changes, invalid/missing weather and deterministic outputs. |
| `test_rules.py` | Threshold comparisons, overlapping rules and severity precedence. |
| `test_scheduler.py` | Whole activity duration, availability/shift constraints, missing hours, ties and impossible windows. |
| `test_alerts.py` | Grouping, severity, duplicate suppression and meaningful explanations. |

Include explicit expected results from the agreed specification. Do not validate formulas only against copies of the same implementation.
