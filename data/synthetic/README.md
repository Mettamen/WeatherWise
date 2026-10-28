# Original synthetic CSVs — Sam and Metta

These source files are already populated because they are copies of your existing dataset. Do not overwrite them during application development.

| File | Primary user | Purpose |
| --- | --- | --- |
| `00_data_dictionary_and_schema.csv` | Sam + Metta | Read column descriptions, keys, units and constraints before coding. |
| `01_locations.csv` | Sam | City/location reference for APIs and weather lookup. |
| `02_weather_hourly_observed.csv` | Sam -> Metta | Load synthetic hourly weather and pass validated values to the engine. |
| `03_weather_forecast_hourly.csv` | Sam + Metta | Synthetic forecast pipeline experiments; not evidence of real forecast skill. |
| `04_medical_conditions_reference.csv` | Metta | Inspect illustrative condition sensitivities; Sam exposes selections to the UI. |
| `05_occupations_exposure_reference.csv` | Metta | Inspect occupational exposure; Sam exposes selections to the UI. |
| `06_hazard_thresholds.csv` | Metta | Define explicit threshold comparisons and resolve boundary ambiguity. |
| `07_users_health_profiles_synthetic.csv` | Sam + Metta | Fictional test profiles, not real accounts. |
| `08_user_routines.csv` | Sam + Metta | Routine examples; check overlaps before using them. |
| `09_risk_training_dataset.csv` | Metta | Optional ML experiments with leakage-aware splits and honest evaluation. |
| `10_rule_based_decision_table.csv` | Metta | Translate pseudo-logic into tested executable rules. |
| `11_alerts_log.csv` | Sam + Metta | Example delivery/history structure; do not treat simulated actions as real feedback. |
| `12_schedule_optimization_suggestions.csv` | Metta | Inspect known 05:00 bias; design an improved constrained scheduler. |
| `13_authority_verification_records.csv` | Sam | Simulated verification structure; does not verify real health conditions. |
| `14_health_recommendations_library.csv` | Metta | Illustrative advice; review before real-world use. |

Shreshta should consume small agreed API/mock responses rather than reading these full tables in the browser. Weather windows cover 1–14 May and 1–14 November 2026. Keep explicit synthetic labels even when dates are in the past.
