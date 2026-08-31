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
| Phase 3B — Private Operational State Bootstrap | COMPLETE | Separate private operational-state layer established, pinned to public method version, validated fail-closed |
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

## Current priority

### Phase 3R — Radar Precision Upgrade v0.1

The existing news-push conversation remains the user-facing presentation layer. The current priority is to upgrade the backend World Intelligence Engine from conceptual Draft 0.2 into a stateful, precise systemic-risk radar before continuing deeper physical-capability audits.

Priority focus:
- source/evidence precision;
- event fingerprinting and dedup;
- behavior vs rhetoric;
- counterevidence/falsification;
- A/B/C/D edge and coupling deltas;
- alert suppression/hysteresis;
- first Chain Watch: climate→food/energy→inflation→Fed→UST/financial conditions→AI CapEx/valuation.

### Phase 3C — Capability Verification & Baseline Completion — PAUSED AFTER CLEAN CHECKPOINT

Phase 3B has established a separate private operational-state layer and validated it against a pinned public method version. Water baseline has been instantiated in private state; Water field evidence collection remains open. Energy verification method v0.1 is complete in the public method repository.

The next task is to move private capabilities from `stated` toward `measured` / `field_tested` / `audited`, fill missing required domains, identify real single points of failure, and only then derive defensible Base Autonomy / First Failure Point.

Public `main` must continue to contain methods and aggregate status only. Real private values remain outside this repository.

Until sufficient private coverage exists, the system must keep real Base Autonomy and Personal R-Level fail-closed rather than inventing certainty.
