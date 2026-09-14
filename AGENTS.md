# AGENTS.md — Personal Systemic Risk & Resilience OS

This file is the mandatory entry point for any ChatGPT, Codex, Desktop, CI, or other engineering agent working on this project.

## 0. Engineering truth and fail-closed startup

The project uses two repositories:

- PUBLIC method repository: `yeqilei0328-creator/personal-systemic-risk-resilience-os`
- PRIVATE operational-state repository: `yeqilei0328-creator/personal-systemic-risk-resilience-state`

GitHub `main` is authoritative for each repository within its authority boundary. Conversation history, model memory, local worktrees, old SHAs, issue comments and unmerged branches are evidence/navigation only.

If repository state is `UNKNOWN`, `MISSING`, `DRIFTED`, `STALE`, `UNVERIFIED`, `UNAUTHORIZED`, or contains `CONFLICTING_EVIDENCE`, stop the affected path with `FAIL_CLOSED`.

Rules, State and Evidence are separate concepts and must not be silently merged.

## 1. Mandatory startup sequence

Before substantial implementation:

1. Fresh-read PUBLIC `main`:
   - `AGENTS.md`
   - `WORKFLOW.md`
   - `docs/PROJECT-ENGINE.md`
   - `docs/ENGINEERING-AUTONOMY-GOVERNANCE.md`
   - `docs/EXECUTION-ROUTER.md`
   - `docs/TECHNOLOGY-RADAR-GATE.md`
   - `docs/REALITY-FIRST.md`
   - `docs/STRATEGIC-CAPTURE.md`
   - `docs/GOVERNANCE-EVIDENCE.md`
   - `config/governance.json`
   - `docs/PROJECT-STATE.md`
   - `docs/ROADMAP.md`
   - current-domain method/schema/docs
   - open Issues / PRs
   - current CI

2. Fresh-read PRIVATE `main` only when authorized and necessary:
   - `AGENTS.md`
   - `docs/STATE-OPERATING-MODEL.md`
   - `state-manifest.json`
   - `vendor/method-pin.json`
   - `preparedness/current.json`
   - current-domain audit/assessment/plan
   - open Issues / PRs
   - current CI

3. Recover the current checkpoint before writing:
   - PUBLIC main SHA
   - PRIVATE main SHA when in scope
   - branch / HEAD / merge-base
   - active Issue / PR
   - current phase/domain
   - blockers
   - authority state
   - Radar trigger state
   - deferred reality evidence
   - next exact work unit

4. Emit or internally bind the Router Header:

```text
AUTHORITY_ROUTER = GREEN / AMBER / RED
EXECUTION_ROUTER = GPT_ONLY / GPT_DESKTOP / GPT_DESKTOP_CODEX
MODEL_ROUTER = LUNA / TERRA / SOL / ASTRA
REASONING_EFFORT = LIGHT / MEDIUM / HIGH / EXTREME
FALLBACK_ROUTER = <explicit fallback>
```

Do not ask the user to reconstruct repository state that GitHub can establish.

## 2. Authority Router

Capability is not authority.

### GREEN
May proceed autonomously when otherwise in scope:
- read/search;
- local deterministic edits;
- branch creation;
- local/focused/full tests;
- dry-run and simulation;
- read-only APIs;
- report/evidence generation;
- CI diagnosis that causes no real-world side effect.

### AMBER
Requires explicit review/approval before the governance change is accepted:
- governance/workflow change;
- critical schema change;
- permission router change;
- dependency or architecture widening;
- security boundary change;
- method-pin contract change.

AMBER does not grant RED authority.

### RED
Requires fresh Owner authorization bound to exact scope/gate and must be bounded:
- production write;
- write of sensitive/private operational state outside an already-authorized bounded transaction;
- credential/account mutation;
- payment/procurement;
- camera/microphone/device access or control;
- robot/drone/vehicle/PLC/arm/physical dispatch;
- destructive action.

For RED:
- authorization granted is not the same as authorization consumed;
- define the exact consumption boundary;
- after RED is consumed, automatic retry is `0`;
- a later attempt requires diagnosis, a new exact gate and fresh Owner authorization;
- no Radar result or agent capability may silently widen RED authority.

Canonical authority contract: `docs/ENGINEERING-AUTONOMY-GOVERNANCE.md`.

## 3. PUBLIC / PRIVATE authority boundary

PUBLIC `main` is authoritative for:
- architecture;
- schemas;
- algorithms;
- verification methods;
- risk logic;
- public-safe synthetic examples;
- Project Engine and public governance.

PRIVATE `main` is authoritative for:
- real capability state;
- real evidence and measurements;
- real dependencies / SPOFs;
- real operational topology;
- preparedness snapshot;
- real autonomy / first-failure state when defensible.

Never write real private values into the PUBLIC repository. Never place secrets in either repository.

## 4. Method pin invariant

PRIVATE state must be interpreted by a pinned PUBLIC method.

Before advancing `vendor/method-pin.json`:
1. compare every existing vendored file SHA with the candidate PUBLIC `main`;
2. require unchanged files to match or perform an explicit migration;
3. vendor the new method/schema files;
4. update the pin;
5. recompute stored assessments with the pinned code;
6. require PRIVATE CI PASS.

Do not silently mix methods from different public commits.

## 5. Canonical work-unit lifecycle

Every material work unit follows:

```text
READ
→ INHERIT PARENT DECISION
→ RADAR TRIGGER CHECK
→ AUTHORITY ROUTER
→ EXECUTION ROUTER
→ PLAN
→ IMPLEMENT
→ FOCUSED TEST
→ FULL REGRESSION
→ STATIC / INTEGRITY
→ SELF-AUDIT
→ PR
→ CI
→ EXACT-HEAD GATE
→ MERGE
→ POST-MERGE VERIFY
→ DURABLE CLOSEOUT
→ NEXT AUTHORIZED WORK UNIT
```

Re-enter routing on unknown, drift, blocker, authority change or reality failure.

Full workflow: `WORKFLOW.md`.

## 6. Radar namespaces are distinct

Three different systems exist and must not be conflated:

1. **Systemic-Risk Radar** — the product intelligence engine that observes world-risk change.
2. **Technology Radar** — engineering prior-art/reality control. Canonical: `docs/TECHNOLOGY-RADAR-GATE.md`.
3. **Commercial/Ecosystem Radar** — vendor/platform/procurement/market-assumption discovery or validation when those external claims can change an engineering or readiness decision. Canonical: `docs/COMMERCIAL-RADAR.md`.

Technology Radar and Commercial/Ecosystem Radar are deterministic trigger outcomes. When triggered they stop local speculation, permit read-only evidence capture and require GPT Control Plane reconciliation before implementation resumes.

Radar never grants merge, production, credential, procurement, device or other RED authority.

## 7. Reality-First and Strategic Capture

This project already owns `R0-R5` for **Personal Action Level**. Therefore Reality maturity uses the collision-safe namespace:

```text
RL0 assumption
RL1 mock
RL2 simulated integration
RL3 local integration
RL4 first real signal
RL5 repeatable real signal
RL6 operational confidence
```

Do not infer a higher Reality level from code/test success alone.

Use bounded Reality Spikes: one path, one environment, one attempt, one evidence bundle unless a different bounded envelope is explicitly approved.

Repeated failure must stop. After the configured repeated-failure / spike budget is exhausted, enter `STRATEGIC_CAPTURE`; do not prepare an infinite next attempt.

Canonical contracts:
- `docs/REALITY-FIRST.md`
- `docs/STRATEGIC-CAPTURE.md`

## 8. Domain execution loop

For each capability domain:

### A. PUBLIC method
If a verification method is missing:

`Issue → branch → Fresh Read → Radar trigger check → routers → schema → deterministic logic → synthetic examples → tests → docs → unified validator → PR → exact-head CI → review → merge → post-merge verify`.

### B. PRIVATE baseline
After PUBLIC method merge, and only when authority permits:

`pin audit → vendor method → restricted audit → deterministic assessment → field/measurement plan → capability link → manifest → private validator → PR → exact-head CI → review → merge → post-merge verify`.

### C. Evidence discipline

`stated ≠ measured ≠ field_tested ≠ audited`

Ownership is not autonomy. Unknown remains unknown. Stored assessments must equal deterministic derivation from the pinned method.

## 9. Model First → Batch Field Validation

Do not interrupt every domain with immediate field work.

Default:
1. build method;
2. instantiate a conservative PRIVATE baseline;
3. infer dependencies, SPOFs, blockers and missing evidence;
4. write field-test plan;
5. continue through the modelling wave;
6. consolidate field work;
7. obtain the required RED authorization envelope before real device/site execution;
8. collect evidence;
9. recompute assessments and Preparedness.

Current survival model remains:
**Water + Energy + Communications / Network / Offline Compute + Food**, then **Mobility → Sanitation → Medical**.

## 10. Fail-closed domain rules

Do not invent:
- autonomy days;
- availability;
- independent communication paths;
- potability;
- islanding / black-start;
- agricultural suitability;
- scenario probability;
- Personal R-Level.

`拥有 ≠ 可用；可用 ≠ 可持续；可持续 ≠ 自给。`

## 11. Exact-head / Merge / Post-merge discipline

A PASS is meaningful only when bound to an exact SHA.

Record:
```text
tested_head
pr_head
origin_main
merge_base
```

Before merge require:
- focused PASS;
- full regression PASS;
- static/integrity PASS;
- CI PASS on exact PR head;
- base/current-main reconciliation;
- mergeable CLEAN;
- no unresolved review/thread;
- scope/privacy/secret/authority clean.

Governance changes must not weaken RED, merge gates or Owner gates.

`PR MERGED` is not completion. Completion is:

```text
MERGED
+
POST_MERGE_VERIFIED
```

## 12. Stale branch reconciliation

If `main` advances with foundational changes after a feature branch was created, do not merge the stale branch blindly.

Foundational classes include:
- Project Engine / AGENTS / WORKFLOW / governance contracts;
- Technology Radar contract;
- validators;
- state-manifest contracts;
- security rules;
- method-pin / schema contracts.

Fresh-read current `main`, compare branch base and overlap, reconcile on top of current `main`, rerun exact-head CI and merge only the reconciled result.

Mergeability alone is not proof of governance safety.

## 13. Security / privacy / local-path discipline

PUBLIC must not store:
- balances/liabilities/cash flow;
- identifiable site inventories or exact capacities;
- real network/security topology;
- credentials/tokens/private keys/recovery codes;
- people/contact lists;
- exact private routes;
- sensitive Physical AI deployment details;
- raw camera/microphone identifiers;
- personal local filesystem paths;
- pixel/biometric traces.

PRIVATE may store bounded operational evidence but still never secrets.

Prefer SHA, generic classes, aggregate statistics and sanitized metadata.

## 14. Physical AI authority

Physical AI in this project remains defensive/non-weaponized.

Any real physical execution requires a Physical Execution Authority Envelope defining:
- device;
- operation;
- duration;
- environment;
- allowed commands;
- forbidden commands;
- stop condition;
- retry policy;
- evidence.

Keep proposal, approval, execution and verification separate.

An AI-generated `TaskProposal` is non-authoritative by default and cannot directly actuate a device.

Canonical contract: `docs/PHYSICAL-AUTHORITY.md`.

## 15. Durable evidence and handoff

Before ending a significant engineering session, durable state must make the next authorized action reconstructable without chat archaeology.

Record as applicable:
- exact PUBLIC / PRIVATE main SHAs;
- exact tested/pr head and merge-base;
- current phase/domain;
- Issue / PR;
- Router Header;
- Radar result;
- Reality level/debt;
- tests and CI;
- authority granted/consumed state;
- retry state;
- evidence fingerprint;
- known unknowns;
- next authorized node.

Canonical evidence contract: `docs/GOVERNANCE-EVIDENCE.md`.

## 16. Canonical control documents

Read these as one control plane:
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/PROJECT-ENGINE.md`
- `docs/ENGINEERING-AUTONOMY-GOVERNANCE.md`
- `docs/EXECUTION-ROUTER.md`
- `docs/TECHNOLOGY-RADAR-GATE.md`
- `docs/COMMERCIAL-RADAR.md`
- `docs/REALITY-FIRST.md`
- `docs/STRATEGIC-CAPTURE.md`
- `docs/PHYSICAL-AUTHORITY.md`
- `docs/GOVERNANCE-EVIDENCE.md`
- `config/governance.json`
- `docs/PROJECT-STATE.md`

If they conflict, stop the affected path as `CONFLICTING_EVIDENCE` and reconcile current `main`; do not choose whichever text is convenient.