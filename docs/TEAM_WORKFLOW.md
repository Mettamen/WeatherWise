# Team workflow

## Ownership

Sam owns Backend 1, Metta owns Backend 2, and Shreshta owns frontend. Each person should work primarily in their named folder and corresponding tests. Folder READMEs explain every placeholder file.

Shared files need coordination: Sam maintains dependency/config files, scripts and API contracts; Metta maintains the risk specification; Shreshta maintains frontend assets and mocks. All three agree on scope, response shapes and integration behaviour.

## Work separately without breaking integration

1. Keep the complete project in the shared repository: https://github.com/Mettamen/WeatherWise. Clone it locally so every teammate has the full structure.
2. Each teammate uses a separate branch, such as `sam/be1`, `metta/be2` and `shreshta/frontend`.
3. Agree on the API contract before writing dependent code.
4. Sam can build routes using temporary agreed calculation outputs while Metta develops the engine.
5. Metta can test the engine with small fictional input objects independently of the API.
6. Shreshta can build against fixed agreed mock responses before either backend is ready.
7. Integrate small changes regularly; review changes to shared interfaces with both other owners.

## Avoid overlapping responsibilities

- Sam handles data retrieval, access checks, persistence and delivery; Metta handles the meaning of risk and recommendations.
- Shreshta renders API outputs and handles interactions; do not duplicate the risk model in browser code.
- Metta produces alert events; Sam sends them; Shreshta displays them and captures preferences.
- Metta ranks outdoor windows; Sam provides routines/weather; Shreshta edits routines and presents results.
- Raw datasets remain unchanged. Derived data should have separate names, provenance and generation instructions.

## First team milestone

Build one complete path: fictional profile + synthetic weather → personal score and explanation → dashboard. Add scheduling, alerts and other features once this path works.

Before a merge, run relevant tests, update your documentation, check that the other teams' interfaces remain compatible, and have a teammate review the change. Write actual setup commands in the main README only when those commands work.
