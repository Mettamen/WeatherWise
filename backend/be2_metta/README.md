# Metta — Backend 2 (BE2)

**Owner: Metta.** You write the code in every file in this folder. Files are intentionally empty.

| File | What you should implement |
| --- | --- |
| `__init__.py` | Python package marker; may remain empty. |
| `service.py` | One entry point taking profile, weather and routines, returning the combined personal outlook for Sam's API. |
| `risk.py` | Personal risk score and risk band from weather, condition sensitivities, age, occupation and exposure. |
| `rules.py` | Executable heat/rain/AQI/UV rules with explicit boundaries and precedence. Resolve conflicts in the supplied pseudo-rules. |
| `recommendations.py` | Select clear advice and explanations from hazards/profile; separate illustrative content from reviewed guidance. |
| `scheduler.py` | Rank complete outdoor activity windows within actual availability, shifts and travel constraints. |
| `alerts.py` | Decide when to create an alert, its severity, grouping, priority and deduplication key. Sam handles delivery. |
| `features.py` | Build consistent model/rule features from inputs; prevent target leakage. |
| `train_model.py` | Optional later training pipeline with documented features, grouped/time-aware splits and saved model metadata. |
| `evaluate_model.py` | Compare against rule baselines and report metrics by class/user group; separate synthetic agreement from real validation. |

## Suggested order

1. Agree on shared input/output types with Sam and Shreshta.
2. Document the intended scoring formula in `docs/RISK_MODEL.md` before implementation.
3. Build and test deterministic rules and explanations first.
4. Implement full-duration time-window ranking and grouped alert events.
5. Connect the service to Sam's routes using the agreed contract.
6. Only then work on ML if it remains in the project scope.

## Known source-data issues to address

- All supplied schedule suggestions use 05:00. Do not copy this behaviour; respect the user's real availability.
- The original risk labels and pseudo-rules can disagree. Define which rules override other scores.
- A zero-hazard hour needs a `none` hazard state rather than automatically becoming heat.
- Synthetic risk labels are formula-derived. A model learning them does not establish clinical prediction accuracy.
- The current condition list does not cover communicable-disease surveillance. Agree on scope before implementing that user story.

## Boundaries and handoff

Keep this layer independent of the database, HTTP and frontend. Return structured results rather than HTML. Ask Sam to supply cleaned inputs. Explain each field's meaning to Shreshta. Put tests in `tests/be2_metta/`.

Done means reproducible scoring, tested threshold boundaries, feasible windows, explainable alerts and documented limitations. No calculation code is implemented yet.
