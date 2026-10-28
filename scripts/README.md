# Development scripts — Sam

These files are empty placeholders; none can start or configure the app yet.

| File | What to implement |
| --- | --- |
| `setup.ps1` | Check Python version, create a local environment and install agreed dependencies. |
| `run.ps1` | Start the backend and explain the local webpage URL. |
| `frontend.ps1` | Start Shreshta's independent static/mock frontend preview, or call the chosen framework dev server. |
| `check.ps1` | Run agreed backend and integration tests; stop on failures. |
| `export_contracts.py` | Generate the agreed OpenAPI/schema and mock responses after backend contracts exist. |

Keep scripts portable across team computers; do not hardcode Metta's Downloads paths. Document exact commands in the root README when the scripts are implemented.
