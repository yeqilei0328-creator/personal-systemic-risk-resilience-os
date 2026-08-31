# World Intelligence Engine — Phase 3R

## Status

**Operational baseline preserved and reconciled.**

Canonical baseline:
- `docs/reference/CHINA_INTELLIGENCE_PUSH_AND_RUNTIME_ARCHITECTURE_V0.3.md`
- `docs/NEWS-RADAR-BASELINE.md`
- `docs/NEWS-RADAR-V0.3-RECONCILIATION.md`

The existing news-push conversation remains the user-facing product.

Phase 3R does **not** redesign the recommendation logic. It turns the already-working V0.3 logic into a stateful, replayable Intelligence OS.

## Preserved V0.3 operating logic

- Multi-source Discovery
- Candidate Event Pool
- Cluster / Deduplicate
- Atomic Claim Split
- Evidence Acquisition
- Independence / Provenance
- Claim Grade A-D
- Evidence · Behavior · Systems
- Costly Signal
- Rhetoric–Action Gap
- Narrative Gap
- Counter-evidence
- Material Change
- P0-P3
- Physical AI engineering relevance
- Global Risk Resonance
- Judgment Ledger
- Posterior Revision
- No-push discipline

## Canonical runtime pipeline

`Discovery`
→ `Candidate Event Pool`
→ `Event Fingerprint / Cluster / Dedup`
→ `Atomic Claims`
→ `Evidence / Provenance / Source Lineage`
→ `Claim Grade`
→ `Evidence · Behavior · Systems`
→ `Material Change`
→ `Risk / Engineering Relevance`
→ `Structural Delta`
→ `Alert Gate`
→ `Front-end Compression`
→ `Judgment Ledger`
→ `Posterior Revision`

## Time windows

- T0: 0-24h
- T1: 3-15d
- T2: 30-90d

The system must compare across windows rather than treating every 24h headline as new.

## Namespace discipline

Two unrelated A/B/C/D systems exist:

### Claim Grade A-D
Epistemic confidence.

### Risk Variable A-D
- A Geopolitical Competition
- B Resource & Climate Constraints
- C Debt & Financial Cycle
- D Technology & Capital Cycle

Never write bare A/B/C/D where the namespace is ambiguous.

## Persistent objects

Phase 3R should build, in order:

1. Source Registry
2. Source Reputation Ledger
3. Event Store
4. Claim Store
5. Evidence Graph
6. Judgment Ledger
7. Alert History
8. System State Graph
9. Risk Coupling Graph

Physical AI Tech Radar remains authoritative inside the Physical AI project.

## R1 — Source / Evidence Persistence

First implementation node.

Must support:
- source identity;
- source class/tier;
- domain × claim-type reputation;
- primary/secondary/derivative lineage;
- independent-source grouping;
- access status/paywall/robots/partial-read;
- correction history;
- anonymous-source dependence;
- claim-level provenance;
- source concentration;
- timestamps and freshness.

Low-reputation sources are not globally banned; they may still serve narrative/anomaly discovery while being unable to independently upgrade facts.

## R2 — Event / Claim State

Persist:
- stable event fingerprint;
- first_seen / last_updated;
- cluster identity;
- atomic claims;
- claim type;
- dynamic-number timestamp/source/confidence;
- Material Change;
- update-vs-new-event relation.

## R3 — Behavior / System Delta

Persist:
- observable behavior;
- costly-signal dimensions;
- rhetoric-action gap;
- narrative gap;
- counterevidence;
- omitted-variable candidates;
- Risk Variable mapping;
- Edge delta;
- Coupling delta;
- Buffer delta;
- Scenario delta.

The five V0.3 Global Risk signals remain observation channels, not five independent causal votes.

## R4 — Precision alert gate

Preserve:
- P0-P3;
- Trigger A/B/C;
- no-push discipline.

Add:
- common-cause correction;
- model-state delta;
- cooldown;
- hysteresis;
- material-change minimum;
- duplicate suppression.

Default:
**no substantive change = no notification**.

## R5 — Judgment memory

The radar must remember:
- what it believed then;
- why;
- source limitations;
- predicted paths;
- watch signals;
- later result;
- posterior update;
- error type.

This supports calibration of both sources and the system itself.

## R6 — Chain Watch

First tracked chain:

Climate / El Niño
→ Food & Energy
→ Inflation / Inflation Expectations
→ Fed / Monetary Policy
→ UST 10Y / 30Y + Financial Conditions / Fiscal Pressure
→ AI CapEx / Tech Valuation / Financing Stress

Every link tracks:
- Fact
- Forecast
- Correlation
- Causality
- Counterevidence
- Material Delta

## Physical AI branch

Physical AI remains a fixed module in the user-facing intelligence product.

Project-relevant signal flow:

`Active discovery | User-supplied observation`
→ verify / dedup / cluster / compress
→ news-side Action Tag
→ project handoff request
→ TECH-RADAR-04 admission
→ existing Physical AI Technology Radar governance

News-side Action Tags do not grant engineering authority.

See `docs/PHYSICAL-AI-RADAR-INTEGRATION.md`.

## Front-end contract

Preserve simplicity:
- max ~3 top judgments;
- P0-P2 output;
- event = what happened / judgment / why it matters / next observable;
- optional dispute/uncertainty;
- Physical AI only when engineering-relevant;
- Global Risk condition watch remains normally silent.

Backend complexity is a filtering mechanism, not a UI requirement.
