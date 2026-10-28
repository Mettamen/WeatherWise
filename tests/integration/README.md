# Integration tests — all three

Sam maintains these files; Metta and Shreshta review acceptance cases.

| File | What to test |
| --- | --- |
| `test_dashboard.py` | Profile + location + weather produce a complete agreed dashboard response with risk, explanations and feasible windows. |
| `test_user_flow.py` | Create/login, edit profile, set routine, view outlook, handle alerts and delete data. |

Metta supplies expected calculation behaviour; Sam wires endpoints/storage; Shreshta checks that the same payload renders correctly. Include failure states, not only successful flows. Files are empty until the application exists.
