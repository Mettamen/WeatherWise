# Data — Sam is custodian, Metta is analysis owner

`synthetic/` contains the 15 CSV files copied unchanged from the supplied Tamil Nadu ZIP. These are reference inputs, not new implementation code.

- Sam: implement loading, reference checks, units and timestamps; keep raw data unchanged.
- Metta: inspect distributions, develop rules/features and document how derived outputs differ from the original labels.
- Shreshta: use only agreed fictional mock payloads; do not load entire health tables directly into the browser.

The package contains 14 data tables with 79,648 rows plus a 163-row dictionary. Everything is synthetic. No real clinical validation, actual encryption or live weather service is established by these files.

Create separate derived data only after agreeing on generation scripts, provenance and ownership. Original documents in Downloads were not changed.
