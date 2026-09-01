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

4. Run the Technology Radar trigger check defined in `docs/PROJECT-ENGINE.md` before substantial implementation. A triggered Radar gate is mandatory and cannot be silently skipped.

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
Issue → branch → Technology Radar trigger check → schema → deterministic logic → synthetic examples → tests → docs → unified validator → PR → CI → review → merge.

### B. Private baseline
After public method merge:
pin audit → vendor method → restricted audit → deterministic assessment → field/measurement plan → capability link → manifest → private validator → PR → CI → review → merge.

### C. Evidence discipline
`stated ≠ measured ≠ field_tested ≠ audited`

Ownership is not autonomy.

Unknown remains unknown.

Stored assessments must equal deterministic derivation from the pinned method.

### D. Permanent Technology Radar discipline

Technology Radar is a permanent Project Engine control, not a project phase or optional research note.

Mandatory triggers:
- **Major Decision Trigger** — before a material architecture, design, technology, hardware, algorithm, dependency, deployment, or strategic-direction commitment/change.
- **Major Blocker Trigger** — when substantial engineering is blocked, repeatedly failing, or likely to have relevant prior art before further custom attempts.

When triggered:
1. stop the affected implementation path;
2. define the exact engineering question/failure;
3. scan appropriate external reality: official documentation, GitHub repositories/issues/PRs, standards, papers, hardware/software ecosystems, credible deployments and community evidence as appropriate;
4. record reusable prior art, limitations and evidence quality;
5. decide in this order: `REUSE → ADAPT → EXTEND → BUILD`;
6. resume engineering only after the decision is explicit.

**No silent BUILD.** For a material custom implementation, explain why REUSE, ADAPT and EXTEND are insufficient.

Research does not itself authorize installation, production changes, private-state writes, credentials, device connection, or physical control.

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

Current survival modelling priority:
**Water + Energy + Communications / Network / Offline Compute + Food.**

Prepared U1 field work may remain deferred while Food, Mobility, Sanitation and Medical are modelled.

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

## 7A. Stale branch reconciliation

If `main` advances with foundational changes after a feature branch was created, do not merge the stale branch blindly.

Foundational changes include:
- Project Engine / AGENTS
- validators
- state-manifest contracts
- security rules
- method-pin / schema contracts

Before merge:
1. fresh-read current `main`;
2. compare the branch base against current `main`;
3. identify overlapping files;
4. reconcile on top of current `main` or rebuild a clean replacement branch;
5. mark the old branch superseded if replaced;
6. rerun final-head CI.

A branch being mergeable is not proof that it preserves newer controls.

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
- Technology Radar gate/decision when triggered, including unresolved external evidence or reconsideration trigger

The next agent should be able to continue from GitHub without reconstructing the project from conversation history.

## 10. Canonical workflow

Read `docs/PROJECT-ENGINE.md` for the complete operating engine.

If any other project note conflicts with it, current GitHub `main` plus the explicit authority rules in PROJECT-ENGINE take precedence.
