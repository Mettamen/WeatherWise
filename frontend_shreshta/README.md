# Current implementation status

Implemented: the dashboard, profile editor, chart, alerts and time-window views. A full routine editor, real login, translations and map routing remain future work.

The original planning guide below remains for future team work. References below to empty files describe the initial scaffold.

---

# Shreshta — Frontend

**Owner: Shreshta.** You build the webpage in this folder. All code files are empty on purpose.

The initial file layout assumes HTML, CSS and JavaScript modules. You can agree on React or another framework with the team before coding; no framework or dependencies have been chosen or installed for this scaffold.

| File/folder | What you should implement |
| --- | --- |
| `index.html` | Semantic page structure: onboarding/profile, dashboard, hourly forecast, alerts, outdoor windows and routine editor. Add accessible labels and navigation. |
| `styles/` | Brand, layout, responsive behaviour and component styles; see its README. |
| `js/` | Page behaviour, API calls, profile/routine forms and rendering; see its README. |
| `assets/` | Your icons/images/fonts, with attribution where needed. |
| `mock/` | Fixed sample API responses and mock transport so you can work before the backend exists. |

## Suggested order

1. Agree on screen requirements and `shared/API_CONTRACT.md` with Sam and Metta.
2. Build the page layout and mobile styles using mock data.
3. Implement profile and routine forms, validation, loading, empty and error states.
4. Connect the network adapter to Sam's endpoints.
5. Display Metta's risk scores, explanations and recommended windows without recalculating them in the browser.
6. Test keyboard navigation, mobile layouts and end-to-end flows.

## Required states and labels

Show whether weather is synthetic, live or stale. Display sample date and timezone. Do not label a demo result as a real-time warning. Distinguish lower-risk windows from guaranteed safe times. Display unavailable features honestly instead of using decorative buttons that do nothing.

Plan Tamil/English UI if the team keeps that requirement. Real routing/maps require backend spatial data first. Use fictional profiles during development.

## Boundaries and handoff

Keep all HTTP requests in `js/api.js`. Never put credentials/provider secrets in browser files. Sam defines endpoint/auth/error behaviour; Metta defines score/advice semantics. Ask them to update shared contracts before changing response field names.

The page is not runnable yet. Write the code first, then agree on a static development server or framework setup. Do not expect opening the blank index file to show a webpage.
