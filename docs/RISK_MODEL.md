# Demonstration risk and scheduling specification

Owner: Metta. This is a deterministic engineering baseline, not a clinical model. It is newly implemented for this prototype and does not reproduce the original CSV generator or claim validation against observed outcomes.

## Inputs and score

For each hour, let `H` be heat index, `R` rainfall in mm/hour, `A` synthetic AQI and `U` UV index. Let `s_heat` and `s_air` be the maximum corresponding sensitivity weight among the selected conditions (zero if none). `e` is the occupation's supplied outdoor exposure fraction. `a` is 0.15 for age 65 or above and zero otherwise.

```text
heat = max(0, H - 30) × 3 × (1 + 0.45 × s_heat + 0.2 × e + a)
rain = max(0, R - 2.5) × 2.5
air  = max(0, A - 100) × 0.35 × (1 + 0.5 × s_air)
uv   = max(0, U - 5) × 5

score = round(min(100, largest component + 0.15 × sum(other components)), 1)
```

The dominant hazard is the largest component; if all components are zero it is `none`. Ties follow heat, rain, air quality, UV insertion order. The risk bands use the shared boundaries 25, 50 and 75. The daily score is the maximum of the 24 hourly scores.

These coefficients and thresholds are illustrative implementation choices, not cited clinical recommendations. The sensitivity values come from the synthetic reference table and have the same limitation. Occupation affects heat scoring, while activity duration affects the recommended window length; the current score is not a dose model. Humidity contributes through the supplied heat index, not as a separate added component. Cold, pollen, pressure change, infection risk and medication effects are not scored.

## Recommendations and alerts

Advice is selected from fixed messages associated with exceeded thresholds. The engine does not generate diagnoses or recommend medication changes. For selected heart-failure/kidney-disease profiles, heat advice points to an existing clinician fluid plan rather than prescribing an amount.

Alerts begin at score 25. Adjacent hours with the same dominant hazard are combined. The peak score determines the group's title and advice. Stable IDs include location, time range, peak score and hazard. Up to eight groups are returned in chronological order. Browser dismissal does not suppress underlying calculations.

## Feasible outdoor windows

The scheduler examines every complete consecutive block of the requested duration. It rejects blocks that extend outside availability or bridge missing hours, calculates mean hourly risk, ranks by score then start, and greedily chooses up to three non-overlapping windows. Ties choose earlier starts. A full 24-hour availability window is allowed. Cross-midnight activities are not supported.

Unlike the source suggestions table, this uses the selected date and personal scores rather than the city's average summer heat index. It still does not model commute time, fixed shifts, route exposure or routine conflicts beyond the availability entered in the UI.

## Future model experiments

The 40,000-row risk-training table remains available, but labels were generated from a formula. High accuracy on that table measures agreement with synthetic labels, not clinical prediction. Exclude `risk_score` when predicting `risk_level`, and exclude other target-derived variables such as simulated outcomes. Group held-out users, consider temporal separation, report imbalanced-class metrics and compare against transparent rules. Real forecast correction needs archived forecasts matched to later observations; the noisy synthetic forecast table cannot establish real forecast skill.
