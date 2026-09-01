# AGENTS.md — Personal Systemic Risk & Resilience OS

This file is the mandatory entry point for any ChatGPT, Codex, or other engineering agent working on this project.

## 0. Do not trust chat memory as engineering truth

The project uses two repositories:

- PUBLIC method repository: `yeqilei0328-creator/personal-systemic-risk-resilience-os`
- PRIVATE operational-state repository: `yeqilei0328-creator/personal-systemic-risk-resilience-state`

GitHub `main` is authoritative for both repositories.

A conversation, handoff prompt, Issue body, previous SHA, local checkout, or model memory may be stale. Always fresh-read before changing anything.

## 1. Mandatory startup sequence

Before implementation:

1. Fresh-read PUBLIC `main`:
   - `AGENTS.md`
   - `docs/PROJECT-ENGINE.md`
   - `docs/PROJECT-STATE.md`
   - `docs/ROADMAP.md`
   - current-domain method/schema/docs
   - open Issues / PRs
   - current CI

2. Fresh-read PRIVATE `main` if authorized:
   - `AGENTS.md`
   - `docs/STATE-OPERATING-MODEL.md`
   - `state-manifest.json`
   - `vendor/method-pin.json`
   - `preparedness/current.json`
   - current-domain audit/assessment/plan
   - open Issues / PRs
   - current CI

3. State the recovered checkpoint internally before writing:
   - PUBLIC main SHA
   - PRIVATE main SHA
   - current phase/domain
   - open work
   - current blockers
   - next exact engineering action

Do not ask the user to repeat repository state that can be recovered from GitHub.

## 2. Authority boundary

PUBLIC `main` is authoritative for:
- architecture
- schemas
- algorithms
- verification methods
- risk logic
- public-safe synthetic examples
- public workflow / Project Engine

PRIVATE `main` is authoritative for:
- real capability state
- real evidence
- real dependencies / SPOFs
- real measurements
- real operational topology
- preparedness snapshot
- real autonomy / first-failure state when defensible

Never write real private values into the PUBLIC repository.

Never place secrets in either repository.

## 3. Method pin invariant

PRIVATE state must be interpreted by a pinned PUBLIC method.

Before advancing `vendor/method-pin.json`:
1. compare every existing vendored file SHA with the candidate PUBLIC `main`;
2. require all unchanged files to match, or perform an explicit migration;
3. vendor the new method/schema files;
4. update the pin;
5. recompute stored assessments with the pinned code;
6. require PRIVATE CI PASS.

Do not silently mix methods from different public commits.

## 4. Domain execution loop

For each capability domain:

### A. Public method
If a verification method is missing:
Issue → branch → schema → deterministic logic → synthetic examples → tests → docs → unified validator → PR → CI → review → merge.

### B. Private baseline
After public method merge:
pin audit → vendor method → restricted audit → deterministic assessment → field/measurement plan → capability link → manifest → private validator → PR → CI → review → merge.

### C. Evidence discipline
`stated ≠ measured ≠ field_tested ≠ audited`

Ownership is not autonomy.

Unknown remains unknown.

Stored assessments must equal deterministic derivation from the pinned method.

## 5. Model First → Batch Field Validation

Do not interrupt every domain with immediate field work.

Default workflow:
1. build the method;
2. instantiate a conservative PRIVATE baseline;
3. infer dependencies, SPOFs, blockers and required evidence;
4. write the field-test plan;
5. continue through the current modelling wave;
6. only after the wave is fully modelled, generate one consolidated field work order;
7. collect field evidence in a coordinated site session;
8. update PRIVATE evidence/state;
9. recompute assessments and Preparedness.

Current first field wave:
**Water + Energy + Communications / Network / Offline Compute.**

Field work is not complete until cross-domain dependencies are tested together, especially:
- Water pump ↔ Energy
- Communications/local compute ↔ Energy
- Physical AI ↔ Communications/local compute
- Offline knowledge ↔ local compute

## 6. Fail-closed rules

Do not invent:
- autonomy days
- availability
- independent communication paths
- potability
- islanding / black-start
- agricultural suitability
- scenario probability
- Personal R-Level

when required evidence is missing.

`拥有 ≠ 可用；可用 ≠ 可持续；可持续 ≠ 自给。`

## 7. PR / CI discipline

- Work on a branch.
- Use PR review as the merge gate.
- Validate the final head, not an earlier green commit.
- Merge with the expected head SHA.
- If CI catches a bad fixture but the algorithm is correct, fix the fixture.
- Never weaken a safety/evidence rule solely to make CI green.
- Update Project State/Roadmap only when the implementation state is true.

## 8. Security boundary

PUBLIC repository must not contain:
- balances / liabilities / cash flow
- identifiable site inventories or exact capacities
- real network/security topology
- credentials / tokens / private keys
- people/contact lists
- exact routes
- sensitive Physical AI deployment details

PRIVATE repository may contain operational state but still must not contain secrets.

Physical AI work in this project is defensive/non-weaponized.

## 9. Handoff contract

Before ending a significant engineering session, ensure durable state records:
- exact PUBLIC main SHA
- exact PRIVATE main SHA
- current phase/domain
- merged work
- open Issue/PR
- CI state
- private evidence still missing
- next exact action
- whether field work is deferred

The next agent should be able to continue from GitHub without reconstructing the project from conversation history.

## 10. Canonical workflow

Read `docs/PROJECT-ENGINE.md` for the complete operating engine.

If any other project note conflicts with it, current GitHub `main` plus the explicit authority rules in PROJECT-ENGINE take precedence.
