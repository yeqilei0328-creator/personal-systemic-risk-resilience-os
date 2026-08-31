# News Radar Baseline — Canonical after V0.3 Reconciliation

## Status

**CANONICAL OPERATIONAL BASELINE / Phase 3R-00A**

Primary source:
`docs/reference/CHINA_INTELLIGENCE_PUSH_AND_RUNTIME_ARCHITECTURE_V0.3.md`

Reconciliation:
`docs/NEWS-RADAR-V0.3-RECONCILIATION.md`

This baseline preserves the existing working product and makes explicit where Phase 3R adds persistence/precision.

## Mission

This is not a news summarizer.

It converts noisy public information into:
1. China Morning Intelligence Brief;
2. Physical AI Radar;
3. Global Risk Resonance anomaly detection.

Core rule:

> 后台复杂，前台简单；事实先于判断；行为重于语言；系统重于单条新闻；变化重于重复；宁缺毋滥。

## Runtime product shape

### Morning brief
- enabled;
- once daily around 08:00;
- P0-P2 China items;
- includes Physical AI Radar;
- no duplicate evening brief;
- no default hourly P0 presentation loop.

### Global Risk Resonance
- separate condition watch;
- normally silent;
- triggers only on meaningful systemic change.

Runtime scheduling is operational/external. This repository defines logic, state and gates.

## Canonical pipeline

`Multi-source Discovery`
→ `Candidate Event Pool`
→ `Cluster / Deduplicate`
→ `Atomic Claim Split`
→ `Evidence Acquisition`
→ `Independence / Provenance`
→ `Claim Grade A-D`
→ `Evidence · Behavior · Systems`
→ `Importance / Relevance / Coupling`
→ `Material Change`
→ `Structural Delta`
→ `Output / Alert Gate`
→ `Front-end Simplification`
→ `Judgment Ledger`
→ `Posterior Revision`

## Time windows

- T0: 0-24h — discovery / immediate change
- T1: 3-15d — trend / repetition / behavior continuity
- T2: 30-90d — structural context / resonance / capital and policy cycles

## Evidence discipline

Hard rules:
- one media outlet cannot decide what is visible;
- reposts are not independent confirmation;
- “reported” does not mean “fact”;
- official sources are high-value for some claim classes, not universal truth;
- do not fill quotas.

### Claim Grade A-D

- A: confirmed enough for factual use
- B: high-confidence but not fully confirmed
- C: developing / insufficiently verified
- D: analysis / opinion / prediction

Always write **Claim Grade A-D** when ambiguity with Risk Variable A-D is possible.

### Source independence

Count origin/independence, not search-result volume.

### Source Reputation Ledger

Reliability is domain × claim-type specific and updates over time.

Low-reputation sources may still serve:
- narrative monitoring;
- propaganda detection;
- anomaly discovery;
- reverse indicators;
but cannot independently upgrade a claim.

## Event intelligence

Event Cluster identity uses:
Actor + Action + Object + Location + Time Window + Consequence

Same cluster only re-alerts on **Material Change**, such as:
- threat → attack;
- plan → budget;
- budget → procurement;
- procurement → delivery;
- demo → deployment;
- expected price effect → observed price/flow transmission.

## Behavior layer

### Costly Signal

Higher value if behavior:
- consumes real resources;
- persists;
- is difficult to reverse.

### Rhetoric–Action Gap

Observable actions may outweigh low-cost statements.

### Narrative Gap

Separate:
- verifiable behavior;
- interpretation;
- emotional language;
- actor interest;
- audience positioning.

## Counterevidence

Every material hypothesis requires active search for:
- alternative causes;
- omitted variables;
- stabilizers;
- contradictory behavior;
- disconfirming prices/flows.

## Systems layer

Track:
Actor / Capability / Intent / Action / Constraint / Resource / Relationship / Feedback / Outcome

Do not equate:
Capability = Intent = Action = Outcome.

## Priority axis

Canonical news importance = **P0-P3**.

- P0 system-level
- P1 high impact
- P2 worth recording
- P3 background / normally silent

Morning brief outputs P0-P2.

Priority is separate from Claim Grade and all systemic/personal states.

## Global Risk observation channels

Preserve the V0.3 five signal groups as detection channels:
1. synchronized geopolitical conflict;
2. energy/shipping corridors;
3. East Asia security structure;
4. extreme weather / major disasters;
5. price and real-economy transmission.

They feed, but do not replace, the four first-order Risk Variables.

## Global systemic state

Canonical engine uses:
- Risk Variable A-D;
- Edge H-state;
- Coupling C0-C3;
- Buffer BU/B0-B3;
- Global Stage I-IV;
- Scenario state.

Legacy `Global Systemic Risk Index` is a display compatibility panel only. No aggregate doomsday score.

## Resonance alert candidates

Preserve V0.3:
- Trigger A: 3+ core observation signals materially worsening;
- Trigger B: one major system-changing event;
- Trigger C: new strong coupling edge.

Phase 3R adds:
- common-cause correction;
- Material Change;
- real-world cost/behavior evidence;
- cooldown;
- hysteresis;
- explicit state delta.

No substantive change = no notification.

## Judgment and learning

Persist:
- Judgment Ledger
- Source Reputation Ledger
- Alert History
- posterior updates
- error types
- source limitations
- predicted paths
- disconfirming outcomes

The system audits both sources and itself.

## Access / concentration / dynamic-number discipline

- disclose paywall/robots/access limitations;
- do not pretend full-text verification;
- mark single-source concentration;
- timestamp unstable numbers;
- do not mix old/new casualty, strike, order or funding figures.

## Physical AI Radar

Physical AI is part of the same user-facing product, not a separate news silo.

Evaluate:
- engineering relevance;
- maturity;
- battlefield evidence maturity where applicable;
- architecture/safety/runtime implications.

News-side Action Tags:
- IGNORE
- WATCH
- TECH-RADAR
- ENGINEERING-IMPACT-PROPOSAL

These are handoff intents only. Formal engineering authority remains in the Physical AI project's TECH-RADAR-04 / TECH-RADAR-01 governance.

See:
`docs/PHYSICAL-AI-RADAR-INTEGRATION.md`

## Front-end contract

Daily top judgments: normally max 3.

Per event:
1. what happened;
2. current judgment / Claim Grade;
3. why it matters;
4. next observable;
5. optional unresolved point.

Global Risk alerts remain short and explain:
- what changed;
- what is resonating;
- why this is not ordinary bad-news accumulation;
- current systemic state;
- 30-90d observables.

## Silence is a valid result

Remain silent for:
- duplicate news;
- rhetoric without action;
- ordinary PR;
- single weak paper;
- battlefield propaganda;
- one isolated fluctuating risk dimension;
- news-density increase without transmission;
- no real cost signal;
- no engineering impact.

> 只有真正值得打断用户时才打断。

## Phase 3R upgrade target

Do not redesign recommendation logic.

Engineer persistence and precision:
- Source Registry
- Event Store
- Claim Store
- Evidence Graph
- Source Reputation Ledger
- Judgment Ledger
- System State Graph
- Risk Coupling Graph
- Alert History
- event fingerprint/dedup
- structural delta
- suppression/hysteresis
- Chain Watch
- replay/backtest
