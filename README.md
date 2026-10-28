# WeatherWise

A responsive local web prototype built around the supplied synthetic Tamil Nadu dataset.

## Run

Python 3.11 or newer is required (tested with 3.12).

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
powershell -ExecutionPolicy Bypass -File scripts/run.ps1
```

Open http://127.0.0.1:8000. The virtual environment is already installed in this workspace. Other team members should run setup first. Stop the server with Ctrl+C.

## Features implemented

- Responsive dashboard with synthetic weather for ten cities and 28 sample days.
- Fictional profile editor with age, conditions, occupation, availability and activity length.
- Explainable illustrative risk scoring, selectable hourly chart and relative outdoor-window rankings.
- In-app alerts with dismiss/restore; profile deletion and reset.
- Anonymous per-tab demo sessions with SQLite persistence and 24-hour expiry.
- Shared schemas, fixed frontend mock fixtures and backend/integration tests.

The data is synthetic, and the rules are demonstration logic, not a clinically validated model. Use fictional profile details only. Profile storage is not encrypted. No live weather, real accounts, push/SMS, route maps, communicable-disease predictions or trained ML models are implemented.

## Team ownership

| Owner | Folder | Implemented files |
| --- | --- | --- |
| Sam / BE1 | backend/be1_sam/ | app.py, repository.py, storage.py |
| Metta / BE2 | backend/be2_metta/ | risk.py, scheduler.py, alerts.py, service.py |
| Shreshta | frontend_shreshta/ | index.html, styles, js/app.js, api.js, dashboard.js, profile.js, format.js, mock transport |

Other previously created code files remain empty future-work placeholders. The original folder READMEs describe the broader planned division of work; see the implementation status note in each folder. The work-allocation PDF remains a planning document.

## Frontend-only development

```powershell
powershell -ExecutionPolicy Bypass -File scripts/frontend.ps1
```

Open http://127.0.0.1:5173/?mock=1. Mock weather and risk values stay fixed; use the integrated backend to test recalculation. Serve over HTTP, not file://.

## Checks and contracts

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1
```

Generated contracts: shared/openapi.json and shared/dashboard.schema.json. After agreed changes, regenerate with `.venv/Scripts/python.exe scripts/export_contracts.py`. The API serves /openapi.json without external documentation/CDN dependencies.

All source CSVs remain unchanged. Weather timestamps use Asia/Kolkata. The current risk calculation is new demo logic, not a reproduction of the original risk-training labels. Its exact formula is documented in docs/RISK_MODEL.md.
