# Testing plan

**No code or tests are implemented yet. Record actual test results here only after the team writes and runs them.**

## Sam — BE1

- Validate profiles, routine inputs and unknown catalog IDs.
- Verify account/session isolation and access checks.
- Test persistence, updates, deletion and database failures.
- Test weather timestamps/units, source mode, missing data and stale-provider failures.
- Verify HTTP responses match the shared API contract.

## Metta — BE2

- Test risk thresholds exactly at and around boundaries.
- Test no-hazard and multiple-hazard conditions.
- Test changed profiles and exposure for expected effects.
- Test complete windows within availability, impossible windows and missing hours.
- Test alert grouping, severity and duplicate handling.
- Check any ML evaluation for leakage and misleading synthetic-data claims.

## Shreshta — frontend

- Test mobile/tablet/desktop layouts without horizontal overflow or clipped text.
- Navigate with keyboard; check form labels, visible focus and modal focus handling.
- Test loading, empty, invalid-input, expired-session and server-unavailable states.
- Test profile/routine save and refresh; confirm the displayed response is current.
- Show clear synthetic/live/stale labels and correct local times.
- Check that all visible buttons work and no console errors occur.
- Verify mock mode is explicit and never silently replaces a failing real API.

## Joint acceptance

Follow a complete user flow from account/profile setup through weather, risk, windows and alerts. Check the UI against the backend payload and Metta's expected calculations. Use fictional data during development.

## Results to fill in later

Record date, revision, environment, test command or browser steps, result and known limitations. Do not report a placeholder file as a passing test.
