# Frontend mocks — Shreshta, with Sam and Metta

Use this folder to work independently before the backend is ready.

| File | Work |
| --- | --- |
| `mock-api.js` | Shreshta: return agreed fixture responses through the same interface as `js/api.js`. Clearly label mock mode. |
| `catalog.json` | Sam supplies example locations, conditions and occupations; Shreshta saves the agreed fixture. |
| `dashboard.json` | Sam and Metta supply the agreed dashboard response; Shreshta uses it to render the UI. |
| `profile.json` | Sam supplies a fictional example profile matching the shared schema. |

JSON files are currently zero-byte placeholders, not valid JSON. Populate them before loading them. Do not invent response shapes independently of `shared/`.
