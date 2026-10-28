# Scope decisions for the team

**This is a planning checklist, not implemented functionality.**

## Suggested first version

- [ ] Fictional adult profile with agreed conditions, occupation and location.
- [ ] Synthetic weather view for the supplied Tamil Nadu cities and dates.
- [ ] Explainable rule-based personal risk.
- [ ] Outdoor-time recommendations that fit availability and activity duration.
- [ ] In-app alerts and preferences.
- [ ] Responsive webpage with loading, empty and error states.

Sam owns the API/data side, Metta owns the calculation side, and Shreshta owns the user interface. Agree together on the final list before coding.

## Decisions still needed

| Decision | Who should lead |
| --- | --- |
| Communicable-disease support in v1 or a later phase | Metta, with the whole team |
| Exact health-profile fields and data storage policy | Sam + Metta |
| Frontend technology and required screens | Shreshta |
| Risk formula, rule precedence and alert thresholds | Metta |
| Weather source and synthetic/live mode transition | Sam |
| Tamil and English coverage | Shreshta, with backend advice support |
| Real accounts versus a fictional demo first | Sam, with the whole team |
| Routes/maps, real notifications and ML experiments | All three |

The supplied screenshot includes communicable and noncommunicable diseases. The current dataset primarily supports chronic conditions and environmental sensitivities; it has no outbreak/transmission data. Resolve this gap explicitly.

Real weather feeds, street-level route ranking, clinical verification, push/SMS and validated ML predictions require additional implementation/data. Keep them out of the UI's claims until they are supported. Treat the supplied medical weights and advice as illustrative while developing the prototype.
