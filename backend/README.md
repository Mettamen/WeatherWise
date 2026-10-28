# Backend workspace

Sam owns Backend 1 (`be1_sam/`). Metta owns Backend 2 (`be2_metta/`).

These are empty starter files, not a working application. Read each person's folder README before coding.

## Division of work

- Sam: server, API endpoints, authentication, database, profiles, weather ingestion and notification delivery.
- Metta: risk calculations, rules, recommendations, scheduling, alert decisions and later ML experiments.
- `__init__.py`: Sam should use this as the Python package marker; it can stay empty.

## Integration boundary

Sam should pass validated profile/weather/routine data to Metta's service. Metta should return structured risk, explanations, advice, time windows and alert events. Agree on those types in `shared/` first. Keep HTTP/database code out of Metta's calculation files.

Suggested stack: Python with FastAPI for the API. Confirm dependencies together before filling the root requirements files.
