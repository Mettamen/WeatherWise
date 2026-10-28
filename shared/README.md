# Shared interfaces — all three teammates

Sam maintains these files after agreement with Metta and Shreshta. These are the only cross-team integration files; discuss changes before editing them.

| File | Work |
| --- | --- |
| `contracts.py` | Sam + Metta: define backend input/output validation types for profiles, routines, weather, risk, alerts and windows. |
| `openapi.yaml` | Sam: document/export methods, paths, authentication, requests, responses and error schemas. |
| `API_CONTRACT.md` | All three: agree on endpoints, field names, units and examples before implementing. |

Code/schema files are intentionally empty. Decide a first contract together, then let each person implement against it. Shreshta may request fields but should not change backend types without agreement.
