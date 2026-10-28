# WeatherWise — team file scaffold

**This is a file structure and task guide only. All application code and configuration placeholders are empty; `.gitignore` contains repository exclusions. Your team will do the coding. There is no runnable webpage or backend yet.**

## Team allocation

| Person | Role | Main folder | Start guide |
| --- | --- | --- | --- |
| Sam | Backend 1 (BE1) | `backend/be1_sam/` | [Sam's README](backend/be1_sam/README.md) |
| Metta | Backend 2 (BE2) | `backend/be2_metta/` | [Metta's README](backend/be2_metta/README.md) |
| Shreshta | Frontend | `frontend_shreshta/` | [Shreshta's README](frontend_shreshta/README.md) |

Every folder contains a README explaining its owner and the purpose of each file.

## Folder layout

```text
WeatherWise/
  backend/
    be1_sam/             API, authentication, database, profiles and weather
    be2_metta/           Risk rules, recommendations, scheduling and ML
  frontend_shreshta/
    index.html           Webpage structure
    styles/              CSS files
    js/                  Browser logic and API adapter
    assets/              Your images/icons/fonts
    mock/                Example responses for independent frontend work
  shared/                Agreed contracts and API specification
  data/
    synthetic/           Original supplied CSVs, unchanged
  scripts/               Empty setup/run/check script placeholders
  tests/
    be1_sam/             Sam's tests
    be2_metta/           Metta's tests
    integration/         Joint acceptance tests
  docs/                  Team workflow, scope, risk spec and testing guide
```

## Root files — Sam maintains these after team agreement

| File | What Sam should write |
| --- | --- |
| `requirements.txt` | Agreed Python runtime dependencies and version constraints. |
| `requirements-dev.txt` | Agreed test/development dependencies. |
| `.env.example` | Environment-variable names with dummy values; never real secrets. |
| `.gitignore` | Basic exclusions are supplied for environments, caches, databases, secrets and build output. Extend as needed. |
| `pyproject.toml` | Agreed Python/test/tool configuration. |

The existing `broke.txt` is your original file and is untouched; it is not part of the scaffold.

## How to begin

1. Everyone reads their folder README.
2. Agree on MVP scope in `docs/SCOPE.md`.
3. Agree on field names, units and endpoint shapes in `shared/API_CONTRACT.md` before coding.
4. Sam builds the API/data layer, Metta builds the calculation layer, and Shreshta builds the UI against agreed mocks.
5. Integrate and test regularly using the shared contract.

Use one shared repository with separate feature branches. Each teammate keeps a complete copy but edits their own files. Do not split the repository into three incomplete projects. Read `docs/TEAM_WORKFLOW.md` for coordination details.

The populated non-document files are the original synthetic CSVs under `data/synthetic/`, `.gitignore`, and your pre-existing local file. Empty JSON/YAML files are placeholders and must be populated before parsing. Setup/run scripts do nothing until Sam writes them.
