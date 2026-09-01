# Project Engine v0.1 — Dual-Repository Operating Workflow

## 1. Mission

The Personal Systemic Risk & Resilience OS exists to preserve agency.

It has two coupled jobs:

1. detect material systemic-risk change early enough to create lead time;
2. convert that lead time into real personal / enterprise / base resilience.

The system is not a doomsday predictor.

A successful system reduces panic because preparation happens before the decision window closes.

> 不是让我比别人更早恐慌，而是让我早到根本不需要恐慌。

---

## 2. The project is one system with two repositories

### PUBLIC METHOD REPOSITORY

`yeqilei0328-creator/personal-systemic-risk-resilience-os`

Role:
- Project Engine
- architecture
- risk model
- schemas
- algorithms
- deterministic verification methods
- public-safe examples
- synthetic replay
- public documentation
- public CI

Visibility: PUBLIC.

### PRIVATE OPERATIONAL-STATE REPOSITORY

`yeqilei0328-creator/personal-systemic-risk-resilience-state`

Role:
- real capability records
- real evidence
- real measurements
- real topology/dependencies/SPOFs
- field-test results
- current preparedness state
- current autonomy / First Failure Point when permitted

Visibility: PRIVATE.

### One system, two authorities

The repositories do not compete.

PUBLIC answers:

> “How should this capability be evaluated?”

PRIVATE answers:

> “What is actually true right now?”

The core boundary is:

> **Open methodology, private exposure.**

---

## 3. Engineering truth hierarchy

When sources disagree, use this order.

### For methodology
1. current PUBLIC `main`
2. current PUBLIC CI / merged code
3. current PUBLIC Project State / Roadmap
4. open PR/Issue execution context
5. conversation history

### For real operational state
1. current PRIVATE `main`
2. current PRIVATE deterministic validator / CI
3. current PRIVATE evidence records
4. current PRIVATE Project State / manifest
5. conversation history

A previous SHA in a prompt is navigation only.

A chat statement is not engineering state until it is persisted appropriately.

---

## 4. Mandatory Fresh-Read Protocol

Every new ChatGPT/Codex session must perform a Fresh Read before implementation.

### PUBLIC Fresh Read

Read:
1. authoritative `main` SHA;
2. `AGENTS.md`;
3. this file;
4. `docs/PROJECT-STATE.md`;
5. `docs/ROADMAP.md`;
6. current domain docs/schema/logic;
7. open Issues;
8. open PRs;
9. latest relevant CI.

### PRIVATE Fresh Read

If authorized, read:
1. authoritative `main` SHA;
2. `AGENTS.md`;
3. `docs/STATE-OPERATING-MODEL.md`;
4. `state-manifest.json`;
5. `vendor/method-pin.json`;
6. `preparedness/current.json`;
7. current domain audit/assessment/measurement plan;
8. open Issues;
9. open PRs;
10. latest relevant CI.

### Recovery output

Before writing code/state, recover:
- PUBLIC SHA
- PRIVATE SHA
- current phase
- current domain
- active branch/PR if any
- blockers
- field evidence deferred
- next exact action

Do not start by trusting the last conversation summary.

---

## 5. The cross-repository transaction

A capability implementation is a two-stage transaction.

### Stage A — PUBLIC method transaction

Trigger:
- capability lacks an adequate verification method;
- existing method needs an explicit revision.

Sequence:

`Issue → branch → schema → logic → synthetic example → tests → docs → validator → PR → final-head CI → review → merge`

Exit:
- method exists on PUBLIC `main`;
- deterministic tests pass;
- method can be vendored.

### Stage B — PRIVATE state transaction

Trigger:
- PUBLIC method exists;
- real capability needs a baseline or evidence update.

Sequence:

`pin audit → vendor method/schema → private audit → deterministic assessment → measurement plan → capability link → state manifest → validator → PR → final-head CI → review → merge`

Exit:
- PRIVATE `main` stores current state;
- stored assessment exactly equals pinned-method derivation;
- raw private values are not emitted in CI logs.

This pairing is the normal Project Engine cycle.

---

## 6. Method-pin protocol

The PRIVATE repository must never mean “latest public code”.

It means:

> **this exact public method version was used to interpret this exact private state.**

### Pin advancement procedure

Before moving the pin:

1. fetch current PRIVATE `vendor/method-pin.json`;
2. for every existing vendored path, compare stored blob SHA with candidate PUBLIC `main`;
3. require all unchanged files to match;
4. if any file drifted, stop and decide whether an explicit migration is required;
5. vendor newly required method/schema files;
6. update `method_commit`;
7. update vendored blob SHAs;
8. run PRIVATE validator;
9. require stored assessments to exactly match deterministic recomputation;
10. merge only after final-head CI PASS.

No silent mixed-version state.

---

## 7. Verification ladder

Canonical ladder:

### stated
User report, document assertion, or observed ownership only.

### measured
A relevant defensible quantity or continuity measurement exists.

### field_tested
The capability works under the relevant degraded/outage condition.

### audited
Field-tested plus evidence completeness, maintenance, independent review and critical dependency/SPOF treatment.

Never promote a state merely because equipment exists.

---

## 8. Fail-closed state

Unknown is a valid engineering result.

The system must prefer:

`unknown`

over:

`probably yes`.

This applies particularly to:
- autonomy
- water potability
- sustainable well yield
- PV islanding
- black-start
- battery usable energy
- communications path independence
- offline-compute continuity
- food autonomy
- agricultural conversion
- mobility degraded-mode range
- Base Autonomy
- First Failure Point
- Personal R-Level

### Preparedness invariant

`Base Autonomy Days = min(critical capability autonomy_days)`

is allowed only after required critical data is sufficiently known.

Otherwise the system remains:
- INCOMPLETE
- UNKNOWN
- DEGRADED

as appropriate.

---

## 9. Model First → Batch Field Validation

### Why

If every capability model immediately stops for a site visit, the project becomes a sequence of disconnected checklists.

Instead, first build a coherent dependency model.

### Default workflow

For each domain in the current modelling wave:

1. build/verify PUBLIC method;
2. create conservative PRIVATE baseline;
3. identify dependencies;
4. identify possible SPOFs;
5. identify what evidence is missing;
6. write a measurement/degraded-test plan;
7. keep unknown values unknown;
8. proceed to the next domain.

After the whole wave is modelled:

9. generate a consolidated field-audit work order;
10. group tests by location, equipment, qualified-person requirement and cross-domain dependency;
11. perform one coordinated field-verification session where practical;
12. attach evidence to PRIVATE state;
13. recompute all affected domains;
14. recompute Preparedness;
15. derive First Failure Point only if allowed.

### Field Wave U1 — Core Utilities / Nervous System

Domains:
1. Water
2. Energy
3. Communications / Network / Offline Compute

Cross-domain checks:
- water extraction power path;
- treatment power path;
- communications resilient power path;
- local compute resilient power path;
- internet-loss local control;
- Physical AI local/degraded operation;
- offline data/knowledge access.

**Do not start repeated site interruptions before U1 modelling is complete.**

At U1 model completion, create one private consolidated:
`FIELD-AUDIT-WAVE-U1.md`

### Next modelling wave

Default next critical sequence after U1:
1. Food
2. Mobility
3. Sanitation / Medical
4. Tools / Spares / Repair
5. Offline Knowledge
6. Industrial Space / Land Conversion
7. Physical AI integration
8. People / Trusted Network

Financial resilience domains remain required but are not confused with the physical field-verification wave:
- cash flow
- liquidity
- asset disposition

---

## 10. Cross-domain dependency engine

Capabilities must not be evaluated as isolated possessions.

Examples:

### Water
depends on:
- source
- pump
- power
- storage
- treatment
- quality
- spares

### Energy
supports:
- water extraction
- communications
- local compute
- refrigeration
- Physical AI
- lighting/security

### Communications
depends on:
- power
- internal network
- upstream external paths
- local compute
- auth/DNS/time/data dependencies

### Physical AI
depends on:
- energy
- communications
- local compute
- maps/models/data
- maintenance/spares
- safe degraded behavior

The engine should prefer a dependency graph over a collection of domain scores.

---

## 11. Single Point of Failure discipline

Potential SPOFs should be identified during modelling.

Real SPOF confirmation should happen after evidence.

Examples:
- one well pump;
- one inverter;
- one router;
- one server;
- one road;
- one person with unique knowledge;
- one provider/upstream;
- one fuel source.

A duplicate of the same dependency is not necessarily redundancy.

Diversity matters.

---

## 12. Radar-to-Preparedness handoff

The Radar and Preparedness engines are coupled but not the same state.

Radar:
- detects material world change;
- updates risk variables/edges/chain/scenario/lead time.

Preparedness:
- maps exposure;
- identifies readiness gaps;
- determines what action becomes justified.

No automatic mapping is allowed from:
- P0-P3
to Stage I-IV,
to R0-R5,
to G0-G4.

Every state transition needs its own explicit rule.

The user-facing news conversation remains the presentation layer for the Radar.

---

## 13. Branch / PR / CI discipline

### Branch
Never build substantial work directly on `main`.

### PR
A PR should state:
- exact base;
- scope;
- invariants;
- evidence boundary;
- non-goals;
- acceptance criteria.

### CI
Always validate the current final head.

An earlier green workflow is not proof for a later head.

### CI failure
Classify first:
- algorithm bug;
- schema bug;
- stale fixture;
- state inconsistency;
- pin drift;
- test bug.

Do not weaken evidence/safety logic just to make CI green.

### Merge
Use expected head SHA when available.

After merge, fresh-read `main` again.

---

## 14. Security engine

### PUBLIC never stores
- real balances / liabilities
- exact private asset capacities
- identifiable property/site details beyond explicitly public-safe abstraction
- real network topology/provider mapping
- credentials/keys/tokens
- personal contacts
- private routes
- sensitive security deployment

### PRIVATE may store
- real operational state
- evidence
- topology
- capacities
- field results

but still never stores:
- passwords
- tokens
- private keys
- recovery codes

### Physical AI
Defensive/non-weaponized only:
- sensing
- patrol/inspection
- fire/smoke detection
- infrastructure inspection
- disaster reconnaissance
- local safe fallback

---

## 15. Decision-quality engine

The project must resist three forms of self-deception.

### Doom bias
Always preserve:
- counterevidence;
- stabilizers;
- alternative explanations;
- hypothesis falsification;
- de-escalation.

### Ownership bias
Do not treat assets as resilience until tested.

### Completion bias
A document/Issue/schema is not completion.

Completion means the relevant exit gate is satisfied and current `main` says so.

---

## 16. Handoff protocol

Every significant session should leave GitHub in a state where a new agent can continue without conversation archaeology.

### Required handoff fields

- PUBLIC repository + exact main SHA
- PRIVATE repository + exact main SHA
- Project Engine version
- current phase
- current domain
- last merged PR
- open PRs
- open Issues
- current CI state
- current PRIVATE method pin
- field evidence deferred
- next exact action
- explicit safety/security boundary

### Rule

If a future ChatGPT/Codex cannot answer “what do I do next?” after reading the two repositories, the workflow is incomplete.

---

## 17. Current execution doctrine

At Project Engine v0.1:

- Phase 3R Radar Precision Upgrade is engineering-complete.
- Phase 3C Capability Verification is active.
- Water public/private baseline exists; field evidence deferred.
- Energy public/private baseline exists; field evidence deferred.
- Communications public method exists; private baseline is the current transaction.
- Field Wave U1 should be executed only after Water + Energy + Communications modelling/baselines/plans are complete.

After U1 modelling:
1. produce one consolidated field-audit work order;
2. review it with the user;
3. collect site evidence;
4. update PRIVATE state;
5. recompute cross-domain dependencies and Preparedness;
6. continue to Food and the next physical-capability wave.

---

## 18. Core project maxims

> 没有改变判断的新闻，不应该打扰你。

> 拥有 ≠ 可用；可用 ≠ 可持续；可持续 ≠ 自给。

> 和平时期追求效率，危机时期追求冗余。

> Internet Down ≠ System Down.

> 云端可增强，本地可独立降级运行。

> 准备越便宜、越通用、越可逆，越早做；准备越昂贵、越极端、越不可逆，触发门槛越高。

> 长期准备看后果，不等概率；短期行动看概率，也看速度。

The final system goal is not maximal stockpiling.

It is:

# Preserve Agency
