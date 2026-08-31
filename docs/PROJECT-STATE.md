# Project State

> GitHub `main` is the authoritative engineering source. Always fresh-read current `main`, Issues, PRs and CI before continuing work. Do not rely on this file alone for commit SHA state.

## Status

Engineering status: **PRE-V1.0 / ACTIVE**

Current completed stages:

| Stage | Status | Durable result |
|---|---|---|
| Phase 0 — Architecture Baseline | COMPLETE | Mission, architecture, risk model, alert taxonomy, intelligence/preparedness principles, red-team rules, public/private data boundary |
| Phase 1 — Core Data Model v0.1 | COMPLETE | Event / Evidence / Edge / Scenario / Exposure / Capability / Alert schemas, synthetic examples, validation |
| Phase 2 — Quantification v0.1 | COMPLETE | Coupling C0-C3, Buffer BU/B0-B3, H-state recommendation, R0-R5 action gates, deterministic tests |
| Phase 3A — Baseline Audit Framework | COMPLETE | Capability audit, Preparedness Snapshot, Base Autonomy / First Failure Point, SPOF detection, private-state integration contract |
| Phase 3B — Private Operational State Bootstrap | BLOCKED / NEXT | Requires a separate private operational-state repository or equivalent private data layer |
| Phase 4 — Playbooks | NOT STARTED | Scenario-to-action playbooks |
| Phase 5 — Red Team & V1.0 Gate | NOT STARTED | Historical calibration, false-positive/false-negative review, action-cost audit, V1.0 approval |

## Current system contract

The system is not a doomsday predictor. It is a Personal Systemic Risk & Resilience OS.

Primary flow:

`World Intelligence → Evidence Verification → Four-Source Risk Model → Coupling/Feedback → Scenario → Exposure → Lead Time / Preparation Window / Disposition Window → Personal Action Level → Preparedness → Playbook`

### Core first-order variables

- A — Geopolitical Competition
- B — Resource & Climate Constraints
- C — Debt & Financial Cycle
- D — Technology & Capital Cycle

### Taxonomies that must remain separate

- P0/P1/P2 — intelligence priority
- Stage I-IV — global systemic stage
- C0-C3 — coupling structure
- BU/B0-B3 — buffer status
- H0/H1/H2/H3/Hx — transmission-edge evidence state
- R0-R5 — personal action level
- G0-G4 — governance integrity

No automatic mapping is allowed between these taxonomies without an explicit decision rule.

## Quantification baseline

The model deliberately does **not** produce one aggregate “doomsday score”.

It reports structural state, including:

- independent cross-variable coupling after common-cause exclusion;
- persistent / H3 transmission strength;
- buffer depletion and coverage gaps;
- edge falsification and counterevidence;
- personal exposure and action-window compression;
- preparedness coverage, autonomy and first failure point.

All numeric thresholds in v0.1 are provisional calibration seeds.

## Preparedness baseline rule

> 拥有 ≠ 可用；可用 ≠ 可持续；可持续 ≠ 自给。

Base Autonomy is fail-closed:

- required domain missing → INCOMPLETE
- critical capability unknown → UNKNOWN
- critical capability unavailable → DEGRADED / 0 days
- sufficiently audited critical capabilities → AUDITED, with autonomy determined by the first failure point

## Public / private boundary

This repository is PUBLIC.

Public `main` may contain:

- methods
- schemas
- algorithms
- audit rules
- playbook templates
- synthetic/public-safe examples

Public `main` must not contain:

- real financial balances, cash flow or liabilities
- identifiable property/site/resource inventories
- exact power/water/food/fuel capacity
- security or communications topology
- credentials or keys
- people/contact lists
- routes or other sensitive operational details

Principle:

> **Open methodology, private exposure.**

## Next engineering node

### Phase 3B — Private Operational State Bootstrap

Required before a real personal/base Preparedness Snapshot can be trusted.

The private state layer will hold real:

- capability audits
- exposures
- finance and asset state
- site/resource state
- communications state
- food/medical state
- people/network state

Every private assessment must pin the public schema/model version used to interpret it.

Until Phase 3B exists, the public repository can define how to measure readiness but must not claim a real Base Autonomy Days or real personal R-Level from incomplete operational data.
