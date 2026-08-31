# Phase 3R-00A — V0.3 Reconciliation

## Status

Source reviewed and reconciled against:
- `docs/NEWS-RADAR-BASELINE.md`
- `docs/INTELLIGENCE-ENGINE.md`
- `docs/PHYSICAL-AI-RADAR-INTEGRATION.md`
- current systemic-risk model and quantification rules

Source of record:
`docs/reference/CHINA_INTELLIGENCE_PUSH_AND_RUNTIME_ARCHITECTURE_V0.3.md`

## Executive decision

V0.3 is the strongest available operational specification for the existing news system.

Phase 3R therefore adopts this rule:

> **Preserve V0.3 operating logic by default; upgrade precision and persistence around it.**

The recovered Phase 3R-00 baseline was directionally correct but incomplete. V0.3 supplies the missing operational detail.

## 1. Preserved without semantic change

The following become canonical Phase 3R inputs:

- multi-source discovery rather than homepage-following;
- original-source preference;
- source-independence checks;
- T0 / T1 / T2 time windows;
- Candidate Event Pool;
- Actor + Action + Object + Location + Time Window + Consequence event clustering;
- Material Change Detection;
- atomic Claim split and Claim-type differentiation;
- Claim Grade A/B/C/D;
- Source Reputation Ledger;
- Evidence · Behavior · Systems;
- Costly Signal Test;
- Rhetoric–Action Gap;
- Narrative Gap;
- active Counter-evidence / omitted-variable search;
- Judgment Ledger;
- Posterior Revision;
- Access Failure disclosure;
- Source Concentration Gate;
- timestamped dynamic-number handling;
- disaster and war claim decomposition;
- market/physical transmission confirmation;
- no-push discipline;
- front-end compression;
- Physical AI maturity ladder and battlefield-evidence ladder;
- Physical AI engineering-relevance filter.

## 2. Namespace collision: Claim Grade A-D vs Risk Variable A-D

V0.3 uses:
- Claim Grade A/B/C/D = epistemic confidence.

The newer systemic-risk model uses:
- Risk Variable A = Geopolitical Competition
- Risk Variable B = Resource & Climate Constraints
- Risk Variable C = Debt & Financial Cycle
- Risk Variable D = Technology & Capital Cycle

These are unrelated.

### Decision

Bare `A/B/C/D` is prohibited in new engineering artifacts where the namespace is ambiguous.

Use:
- `Claim Grade A`, `Claim Grade B`, etc.
- `Risk Variable A`, `Risk Variable B`, etc.

Schemas may preserve existing enums for compatibility, but UI/docs/runtime summaries must carry the namespace.

## 3. P0-P3 restored

The recovered baseline mentioned P0/P1/P2 because those are the normal pushed levels.

V0.3 defines the full importance axis as P0-P3:
- P0 system-level;
- P1 high impact;
- P2 worth recording;
- P3 background / normally silent.

### Decision

Canonical news importance taxonomy = **P0-P3**.

Default morning output remains **P0-P2 only**.

P3 remains useful for storage, context, trend detection and later posterior review.

P0-P3 remains separate from:
- Claim Grade A-D;
- Global Stage I-IV;
- Coupling C0-C3;
- Buffer BU/B0-B3;
- Edge H-state;
- Personal R0-R5;
- Governance G0-G4.

## 4. V0.3 five Global Risk signals vs four first-order variables

V0.3 five signals:
1. geopolitical conflicts;
2. energy/shipping;
3. East Asia security;
4. extreme weather/disasters;
5. price/real-economy transmission.

Newer model:
- A Geopolitical Competition
- B Resource & Climate Constraints
- C Debt & Financial Cycle
- D Technology & Capital Cycle

### Decision

The five V0.3 signals remain **observation / detection channels**.

They are not five independent votes and must not be naively counted as five independent causes.

They feed the A/B/C/D systemic model, where:
- common-cause duplication is removed;
- transmission edges are validated;
- Coupling Density is measured structurally.

This preserves V0.3 discovery strengths while preventing double counting.

## 5. Legacy Global Systemic Risk Index

V0.3 uses a table of domain states:
- low / medium / medium-high / high / extreme;
- trend arrows ↓↓ / ↓ / → / ↑ / ↑↑.

Newer architecture explicitly rejects one aggregate doomsday score and separates:
- Stage I-IV;
- Coupling C0-C3;
- Buffer BU/B0-B3;
- Edge H-states;
- scenario state.

### Decision

The V0.3 `Global Systemic Risk Index` is retained as a **compatibility display panel**, not a canonical scoring engine.

Recommended internal name:
`Global Risk Domain State Panel`

The user-facing legacy label may be preserved where useful, but:
- no hidden aggregate numeric score may be inferred;
- the global-system row must be a derived narrative/state summary;
- canonical decisions come from Stage/Coupling/Buffer/Edge/Scenario state.

## 6. V0.3 resonance triggers A/B/C

V0.3:
- Trigger A: at least 3 of 5 signals clearly worsen;
- Trigger B: one major system-changing event;
- Trigger C: a new strong coupling edge.

### Decision

Preserve all three as compatibility alert candidates.

Phase 3R precision hardening adds:
- common-cause adjustment;
- Material Change requirement;
- independent evidence / real-world cost signal;
- cooldown/hysteresis;
- explicit model-state delta.

Therefore `3 of 5 worsening` is not by itself sufficient if the apparent deterioration is duplicated reporting of one cause with no validated transmission.

## 7. Physical AI Action Tags vs Technology Radar authority

V0.3 news-side Action Tags:
- IGNORE
- WATCH
- TECH-RADAR
- ENGINEERING-IMPACT-PROPOSAL

Physical AI project authoritative layers:
- TECH-RADAR-04 admission routes:
  REJECT / DEFER / WATCH / PROMOTE_TO_V1_RESEARCH / PROJECT_EVIDENCE_RECONCILIATION
- TECH-RADAR-01 decision states:
  ASSESS / TRIAL / ADOPT / HOLD
- authorization ladder:
  RESEARCH < TRIAL < ADOPT < IMPLEMENT < PRODUCTION < PHYSICAL

### Decision

V0.3 Action Tags remain **news-side handoff intents**, not engineering states.

Mapping:
- IGNORE → no project handoff;
- WATCH → retain as news-side watch; TECH-RADAR-04 WATCH only after project admission review;
- TECH-RADAR → request handoff to TECH-RADAR-04;
- ENGINEERING-IMPACT-PROPOSAL → request explicit project architecture/evidence review, never direct implementation authority.

This preserves the useful front-end shorthand while avoiding state collision.

## 8. Physical AI maturity remains separate

V0.3 maturity ladder:
Research → Simulation → Lab Prototype → Real-world Prototype → Pilot → Commercial Deployment → Scaled Deployment

Battlefield evidence ladder is also preserved.

### Decision

Maturity/evidence state describes **how real a technology appears**.

It does not grant:
- TECH-RADAR-01 TRIAL;
- ADOPT;
- IMPLEMENT;
- PRODUCTION;
- PHYSICAL authority.

## 9. Global Risk watch remains an anomaly detector

V0.3 defines:
- morning brief = daily fixed-time briefing;
- Global Risk Resonance = condition watch, normally silent;
- no evening duplicate brief;
- no hourly P0 presentation loop.

### Decision

Preserve this product model.

Scheduling is an operational/external-runtime concern. This repository records semantics and contracts; it does not claim a repository-native scheduler exists unless separately implemented.

## 10. Front-end output contract

Preserve V0.3:
- max ~3 top judgments;
- P0-P2 pushed;
- each event:
  1. what happened;
  2. judgment / Claim Grade;
  3. why it matters;
  4. next observable;
  5. optional unresolved dispute.

Phase 3R adds only decision-relevant structural delta:
- which edge/chain changed;
- whether Stage/Coupling/Buffer/Scenario changed;
- whether personal action changed.

Do not expose backend complexity by default.

## 11. Persistent-object roadmap

V0.3 Appendix B is accepted as the correct Intelligence OS persistence direction:

- Source Registry
- Event Store
- Claim Store
- Evidence Graph
- Source Reputation Ledger
- Judgment Ledger
- System State Graph
- Risk Coupling Graph
- Physical AI Tech Radar
- Alert History

Phase 3R implementation priority:
1. Source Registry + Source Reputation Ledger
2. Event / Claim / Evidence state
3. Judgment Ledger + Alert History
4. System State / Risk Coupling graph integration
5. Chain Watch

## 12. What Phase 3R upgrades rather than preserves

V0.3 already has strong recommendation logic.

Phase 3R therefore focuses on engineering gaps:
- durable state;
- deterministic event fingerprint;
- source lineage;
- automated duplicate/update detection;
- explicit model delta;
- common-cause correction;
- hysteresis/cooldown;
- chain-state persistence;
- falsification/downshift;
- replay/backtest.

The goal is not “better prose”. It is **stateful judgment memory**.

## 13. Canonical one-line architecture after reconciliation

`Multi-source Discovery → Candidate Event Pool → Cluster/Dedup → Atomic Claims → Evidence/Provenance → Claim Grade → Evidence·Behavior·Systems → Material Change → Risk/Engineering Relevance → Structural Delta → Alert Gate → Front-end Compression → Judgment Ledger → Posterior Revision`

Physical AI project-relevant branch:

`Physical AI Signal → Verify/Dedup/Compress → TECH-RADAR-04 Handoff Request → Existing Physical AI Technology Radar Governance`
