# Risk specification worksheet — Metta

**Owner: Metta. No risk model has been implemented in this scaffold.**

Fill in each section as you decide the engine's behaviour. Sam and Shreshta need the resulting input/output contract.

## Inputs

Document weather fields and units, profile attributes, condition sensitivities, occupation/exposure, activity duration and routine context. Specify how to handle unavailable or stale measurements.

## Formula and rule precedence

Write the exact formula or decision tree, its assumptions, and the severity precedence when multiple rules apply. Define all threshold boundaries precisely. Include a no-hazard result. Explain whether a score is an index, a probability or something else; do not imply calibrated probability without evidence.

## Output

Agree on risk score/band, dominant hazard, explanation, guidance, time-window ranking and alert-event fields in `shared/`.

## Scheduling

Define full-activity duration, available hours, fixed shifts, commute/routine conflicts, missing-hour handling and tie-breaking. The source's universal 05:00 suggestion should not become the application's scheduling policy.

## Advice and alerts

Specify reviewed versus illustrative messages, condition-sensitive wording, severity, grouping, deduplication and alert-frequency controls. Separate event creation from Sam's delivery code.

## Evaluation

Document threshold/feasibility tests, baselines and optional model splits. Avoid target-derived features such as using `risk_score` to predict its own `risk_level`. Synthetic-label accuracy measures agreement with the generator, not real-world clinical accuracy.

## Open scope

State which hazards and conditions are covered. Communicable-disease prediction needs additional data and requirements; the current CSV package does not establish that capability.
