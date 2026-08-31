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

- P0/P1/P2/P3 — intelligence priority
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

### Phase 3C — Capability Verification & Baseline Completion — ACTIVE

Phase 3R is engineering-complete. The program has returned to physical/private capability verification.

Current aggregate checkpoint:
- private Water baseline exists and remains `stated`; field evidence pending;
- private Energy baseline exists and remains `stated`; field evidence pending;
- no Water/Energy autonomy claim is permitted yet;
- Preparedness remains fail-closed until required domains and critical capabilities are sufficiently verified;
- next engineering domain: **Communications / Network / Offline Compute Resilience**.

The public repository remains method-only. Real operational values stay in the separate private state layer.

### Phase 3R — Radar Precision Upgrade v0.1 — ENGINEERING COMPLETE

The existing news-push conversation remains the user-facing presentation layer. The current priority is to upgrade the backend World Intelligence Engine from conceptual Draft 0.2 into a stateful, precise systemic-risk radar before continuing deeper physical-capability audits.

Phase 3R-00 and 3R-00A are complete.

The canonical operational baseline is now the reconciled China Intelligence / Physical AI / Global Risk Resonance V0.3 specification. Phase 3R is explicitly an engineering upgrade around that working logic, not a redesign.

R1 Source / Evidence Persistence, R2 Event / Claim State, R3 Behavior / Counterevidence / Structural Delta, R4 Precision Alert Gate, R5 Judgment Memory / Posterior Learning, and R6 Chain Watch are COMPLETE.

Phase 3R node: **ENGINEERING COMPLETE — R1 through R7**.

Next program node: **Phase 3C — Capability Verification & Baseline Completion**, with historical real-world radar calibration retained for Phase 5.

Priority sequence:
- Source Registry + Source Reputation Ledger;
- source independence / derivative lineage / access failures;
- Event + Claim durable state;
- Material Change and event fingerprints;
- Behavior/System structural deltas — complete;
- alert suppression/hysteresis — complete;
- Judgment Ledger / posterior learning — complete;
- first Chain Watch — complete: climate→food/energy→inflation→Fed→UST/financial conditions→AI CapEx/valuation;
- Replay / Red Team — complete;
- 13-case synthetic exit replay — PASS;
- Phase 3R engineering gate — PASS.

Namespace rule:
- `Claim Grade A-D` = epistemic confidence;
- `Risk Variable A-D` = systemic first-order variables;
- bare A/B/C/D is prohibited where ambiguous.

### Phase 3C — Capability Verification & Baseline Completion — ACTIVE

Phase 3B has established a separate private operational-state layer and validated it against a pinned public method version. Water and Energy both have private baseline audits backed by pinned public methods. Both remain at stated verification until field evidence is supplied.

The next task is to move private capabilities from `stated` toward `measured` / `field_tested` / `audited`, fill missing required domains, identify real single points of failure, and only then derive defensible Base Autonomy / First Failure Point.

Public `main` must continue to contain methods and aggregate status only. Real private values remain outside this repository.

Until sufficient private coverage exists, the system must keep real Base Autonomy and Personal R-Level fail-closed rather than inventing certainty.


## Phase 3R completion checkpoint

Phase 3R — Radar Precision Upgrade v0.1 is engineering-complete.

Completed layers:
- R1 — Source / Evidence Persistence
- R2 — Event / Claim State
- R3 — Behavior / Counterevidence / Structural Delta
- R4 — Precision Output / Alert Gate
- R5 — Judgment Memory / Posterior Learning
- R6 — Chain Watch
- R7 — Replay / Red Team

Final synthetic engineering gate:
- 45/45 schemas and synthetic examples validated
- 145 deterministic tests passed
- 13/13 required cross-layer replay cases passed
- synthetic false positives: 0
- synthetic false negatives: 0
- synthetic code mismatches: 0

These results validate the encoded engineering contracts only. They do not establish real-world forecast accuracy.

Real dated-event calibration, false-positive/false-negative estimation on historical evidence, and threshold tuning remain Phase 5 work.

The existing user-facing news-push conversation remains the presentation layer; Phase 3R upgraded the backend precision/state/memory contracts without replacing that presentation workflow.
