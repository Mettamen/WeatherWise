# Browser logic — Shreshta

You own these empty JavaScript files.

| File | Work |
| --- | --- |
| `app.js` | Start the application, manage navigation/state and coordinate refreshes. |
| `api.js` | Centralise API base URL, authentication, requests, response validation and error handling; support an explicit mock mode. |
| `dashboard.js` | Render current/sample weather, risk, advice and hourly outlook. |
| `profile.js` | Profile form, frontend validation, save/edit/delete and consent UI. |
| `routines.js` | Work/activity time-block editor and availability controls. |
| `alerts.js` | Alert list, severity, read/dismiss state and notification preference UI. |
| `scheduler.js` | Display Metta's suggested windows and allow selection; do not implement the risk optimiser here. |
| `format.js` | Shared date/time/unit formatting and safe DOM helpers. |

Use shared API field names. Handle missing, loading and error states. Render user/API text safely and keep secrets out of this folder.
