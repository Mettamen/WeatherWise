# Current implementation status

Implemented: app.py (API/routes), repository.py (catalog/weather), storage.py (demo profiles/sessions). Other code files remain future-work placeholders. Real account authentication is not implemented.

The original planning guide below remains for future team work. References below to empty files describe the initial scaffold.

---

# Sam — Backend 1 (BE1)

**Owner: Sam.** You write the code in every file in this folder. Files are intentionally empty.

| File | What you should implement |
| --- | --- |
| `__init__.py` | Python package marker; may remain empty. |
| `app.py` | Create the API application, register endpoints, configure CORS if needed and connect Metta's service. |
| `config.py` | Load environment settings, database URL and provider credentials; do not hardcode secrets. |
| `database.py` | Database connection, transactions and schema/migration setup. |
| `models.py` | Persistence models for accounts, profiles, routines, preferences and alert history. |
| `auth.py` | Registration/login, password hashing or chosen identity provider, sessions/tokens and protected routes. |
| `profiles.py` | Profile CRUD endpoints, consent, field validation and ownership checks. |
| `routines.py` | CRUD for work/exercise/commute blocks, availability and notification preferences. |
| `weather.py` | Weather-provider adapter, local sample-data loader, timestamps, units, cache and stale-data handling. |
| `repository.py` | Read source CSVs and query/store application records without changing source data. |
| `notifications.py` | Delivery layer for in-app alerts, then optional push/SMS; respect channel preferences and avoid duplicates. |
| `routes.py` | Dashboard/catalog/forecast/history endpoints; call Metta's service and return the agreed contract. |

## Suggested order

1. Agree on request/response types in `shared/` with both teammates.
2. Load locations, conditions, occupations and synthetic hourly weather.
3. Create the API and profile/routine storage.
4. Wire routes to Metta's service; return mock responses until it is ready.
5. Add authentication, access checks and input/error handling.
6. Add real feeds/delivery only after the demo path works.
7. Write your tests in `tests/be1_sam/` and integration checks with the team.

## Files you also maintain

Root dependency/configuration files, `scripts/`, `shared/` (with team agreement), database setup, and data provenance. Your test instructions are in `tests/be1_sam/README.md`.

## Handoff

Give Shreshta endpoint URLs, payload examples and error formats. Give Metta validated inputs with explicit units and timezone. Do not put risk formulas in route handlers or edit Metta's engine without agreement.

Done means endpoints are documented, input and access checks work, data is persisted correctly and frontend integration is tested. No backend is implemented yet.
